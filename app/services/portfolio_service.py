import logging

from sqlalchemy.orm import Session

from app.repositories.portfolio_repo import (
    PortfolioDividendHistoryRepository,
    PortfolioHoldingPerformanceRepository,
    PortfolioRepository,
    PortfolioTradingHistoryRepository,
)
from app.schemas.user import (
    PortfolioCreate,
    PortfolioDetail,
    PortfolioDividendHistoryRead,
    PortfolioHoldingPerformanceRead,
    PortfolioHoldingPerformanceWrite,
    PortfolioIndustryPerformanceRead,
    PortfolioRead,
    PortfolioSectorPerformanceRead,
    PortfolioTradingHistoryRead,
    PortfolioTradingHistoryUpsertRequest,
    PortfolioTradingHistoryWrite,
    PortfolioUpdate,
    PortfolioUpsertRequest,
)

logger = logging.getLogger(__name__)


class PortfolioService:
    """Service for managing portfolios and portfolio data."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._portfolio_repo = PortfolioRepository(session)
        self._holding_repo = PortfolioHoldingPerformanceRepository(session)
        self._trading_repo = PortfolioTradingHistoryRepository(session)
        self._dividend_repo = PortfolioDividendHistoryRepository(session)

    @staticmethod
    def _validate_list(items: list, schema_class):
        """Convert list of items to validated schema instances."""
        return [schema_class.model_validate(item) for item in items]

    def _get_verified_portfolio(self, portfolio_id: int, user_id: int):
        """Get portfolio and verify ownership, raising ValueError if not found or unauthorized."""
        if not self._portfolio_repo.verify_portfolio_ownership(portfolio_id, user_id):
            raise ValueError("Portfolio not found or access denied")

        portfolio = self._portfolio_repo.get_portfolio_by_id(portfolio_id)
        if not portfolio:
            raise ValueError("Portfolio not found")
        return portfolio

    def get_all_portfolios(self, user_id: int) -> list[PortfolioRead]:
        """Get all portfolios for a user."""
        portfolios = self._portfolio_repo.get_all_portfolios(user_id)
        return [PortfolioRead.model_validate(p) for p in portfolios]

    def create_portfolio(
        self, portfolio_in: PortfolioUpsertRequest, user_id: int
    ) -> PortfolioRead:
        """Create a new portfolio for a user."""
        portfolio_data = portfolio_in.model_dump()
        portfolio_data["user_id"] = user_id
        portfolio_create = PortfolioCreate.model_validate(portfolio_data)
        portfolio = self._portfolio_repo.create_portfolio(portfolio_create)
        logger.info(f"Created portfolio {portfolio.id} for user {user_id}")
        return PortfolioRead.model_validate(portfolio)

    def update_portfolio(
        self, portfolio_id: int, portfolio_in: PortfolioUpsertRequest, user_id: int
    ) -> PortfolioRead:
        """Update an existing portfolio for a user."""
        self._get_verified_portfolio(portfolio_id, user_id)

        portfolio_data = portfolio_in.model_dump()
        portfolio_data["id"] = portfolio_id
        portfolio_data["user_id"] = user_id
        portfolio_update = PortfolioUpdate.model_validate(portfolio_data)
        portfolio = self._portfolio_repo.update_portfolio(portfolio_update)
        logger.info(f"Updated portfolio {portfolio.id} for user {user_id}")
        return PortfolioRead.model_validate(portfolio)

    def delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        """Delete a portfolio (soft delete), ensuring it belongs to the authenticated user."""
        self._get_verified_portfolio(portfolio_id, user_id)

        success = self._portfolio_repo.soft_delete_portfolio(portfolio_id, user_id)
        if success:
            logger.info(f"Deleted portfolio {portfolio_id} for user {user_id}")
        return success

    def get_portfolio_details(self, portfolio_id: int, user_id: int) -> PortfolioDetail:
        """Get detailed portfolio information including holdings and trading history."""
        portfolio = self._get_verified_portfolio(portfolio_id, user_id)

        # Fetch all related data
        holdings = self._holding_repo.get_holdings_by_portfolio(portfolio_id)

        # OPTIMIZATION: Load all prices in a single query to avoid N+1
        prices = self._holding_repo.load_current_prices_for_holdings(holdings)
        for holding in holdings:
            holding.set_current_price(prices.get(holding.symbol, 0.0))

        trading_history = self._trading_repo.get_trading_history_by_portfolio(
            portfolio_id
        )
        dividends = self._dividend_repo.get_dividend_history_by_portfolio(portfolio_id)

        # Bulk load company sectors and industries for calculations
        company_sectors = self._holding_repo.load_company_sectors_for_holdings(holdings)
        company_industries = self._holding_repo.load_company_industries_for_holdings(
            holdings
        )

        # Calculate sector and industry performance on-the-fly
        sector_performances = self._calculate_sector_performances(
            holdings, company_sectors
        )
        industry_performances = self._calculate_industry_performances(
            holdings, company_industries
        )

        return PortfolioDetail(
            portfolio=PortfolioRead.model_validate(portfolio),
            holding_performances=self._validate_list(
                holdings, PortfolioHoldingPerformanceRead
            ),
            trading_histories=self._validate_list(
                trading_history, PortfolioTradingHistoryRead
            ),
            dividend_histories=self._validate_list(
                dividends, PortfolioDividendHistoryRead
            ),
            sector_performances=sector_performances,
            industry_performances=industry_performances,
        )

    def buy_holding(
        self,
        portfolio_id: int,
        trading: PortfolioTradingHistoryUpsertRequest,
        user_id: int,
    ) -> PortfolioTradingHistoryRead:
        """Record a buy transaction."""
        # Verify portfolio ownership
        self._get_verified_portfolio(portfolio_id, user_id)

        # Calculate totals
        trade_totals = self._calculate_trade_totals(trading, is_buy=True)
        trade_data = trading.model_dump()
        trade_data.update({**trade_totals, "portfolio_id": portfolio_id})

        trade_write = PortfolioTradingHistoryWrite.model_validate(trade_data)
        response = self._trading_repo.add_trade(trade_write)
        logger.info(
            f"Recorded BUY trade: {trading.shares} shares of {trading.symbol} at ${trading.price_per_share} in portfolio {portfolio_id}"
        )

        # Ensure holding exists for this symbol
        self._ensure_holding_exists(portfolio_id, trading.symbol, trading.currency)
        return PortfolioTradingHistoryRead.model_validate(response)

    def sell_holding(
        self,
        portfolio_id: int,
        trading: PortfolioTradingHistoryUpsertRequest,
        user_id: int,
    ) -> PortfolioTradingHistoryRead:
        """Record a sell transaction."""
        # Verify portfolio ownership
        self._get_verified_portfolio(portfolio_id, user_id)

        # Verify sufficient shares
        holding = self._holding_repo.get_holding(portfolio_id, trading.symbol)
        if not holding:
            raise ValueError(
                f"No holding of {trading.symbol} exists in portfolio {portfolio_id}"
            )

        if holding.total_shares < trading.shares:
            raise ValueError(
                f"Insufficient shares to sell. Have {holding.total_shares}, trying to sell {trading.shares}"
            )

        # Calculate totals
        trade_totals = self._calculate_trade_totals(trading, is_buy=False)
        trade_data = trading.model_dump()
        trade_data.update({**trade_totals, "portfolio_id": portfolio_id})

        trade_write = PortfolioTradingHistoryWrite.model_validate(trade_data)
        response = self._trading_repo.add_trade(trade_write)
        logger.info(
            f"Recorded SELL trade: {trading.shares} shares of {trading.symbol} at ${trading.price_per_share} in portfolio {portfolio_id}"
        )

        # Remove holding if all shares sold
        if holding.total_shares == trading.shares:
            self._holding_repo.delete_holding(holding.id)
            logger.info(
                f"Removed holding {trading.symbol} from portfolio {portfolio_id} after selling all shares"
            )

        return PortfolioTradingHistoryRead.model_validate(response)

    def _calculate_trade_totals(
        self, trading: PortfolioTradingHistoryUpsertRequest, is_buy: bool
    ) -> dict:
        """Calculate total_value and net_total for a trade."""
        total_value = trading.shares * trading.price_per_share
        fees = trading.commission + trading.fees + trading.tax
        net_total = (total_value + fees) if is_buy else (total_value - fees)
        return {"total_value": total_value, "net_total": net_total}

    def _ensure_holding_exists(
        self, portfolio_id: int, symbol: str, currency: str
    ) -> None:
        """Get or create a holding for the given symbol."""
        holding = self._holding_repo.get_holding(portfolio_id, symbol)
        if not holding:
            holding_write = PortfolioHoldingPerformanceWrite(
                portfolio_id=portfolio_id,
                symbol=symbol,
                currency=currency,
            )
            self._holding_repo.add_holding(holding_write)

    def _calculate_sector_performances(
        self, holdings: list, company_sectors: dict[str, str]
    ) -> list[PortfolioSectorPerformanceRead]:
        """
        Calculate sector performance from holdings on-the-fly.

        Args:
            holdings: List of PortfolioHoldingPerformance objects
            company_sectors: Dict mapping symbol -> sector

        Returns:
            List of PortfolioSectorPerformanceRead with calculated metrics
        """
        # Group holdings by sector
        sector_holdings: dict[str, list] = {}
        for holding in holdings:
            sector = company_sectors.get(holding.symbol, "")
            if sector:  # Only include holdings with valid sectors
                if sector not in sector_holdings:
                    sector_holdings[sector] = []
                sector_holdings[sector].append(holding)

        # Calculate performance for each sector
        portfolio_total_invested = sum(h.total_invested for h in holdings)

        sector_performances = []
        for sector, sector_hlds in sector_holdings.items():
            sector_total_invested = sum(h.total_invested for h in sector_hlds)
            sector_total_gain_loss = sum(h.total_gain_loss for h in sector_hlds)
            sector_allocation = (
                (sector_total_invested / portfolio_total_invested * 100)
                if portfolio_total_invested > 0
                else 0.0
            )

            sector_perf = PortfolioSectorPerformanceRead(
                sector=sector,
                currency="USD",
                total_invested=sector_total_invested,
                total_gain_loss=sector_total_gain_loss,
                allocation_percentage=sector_allocation,
            )
            sector_performances.append(sector_perf)

        return sector_performances

    def _calculate_industry_performances(
        self, holdings: list, company_industries: dict[str, str]
    ) -> list[PortfolioIndustryPerformanceRead]:
        """
        Calculate industry performance from holdings on-the-fly.

        Args:
            holdings: List of PortfolioHoldingPerformance objects
            company_industries: Dict mapping symbol -> industry

        Returns:
            List of PortfolioIndustryPerformanceRead with calculated metrics
        """
        # Group holdings by industry
        industry_holdings: dict[str, list] = {}
        for holding in holdings:
            industry = company_industries.get(holding.symbol, "")
            if industry:  # Only include holdings with valid industries
                if industry not in industry_holdings:
                    industry_holdings[industry] = []
                industry_holdings[industry].append(holding)

        # Calculate performance for each industry
        portfolio_total_invested = sum(h.total_invested for h in holdings)

        industry_performances = []
        for industry, industry_hlds in industry_holdings.items():
            industry_total_invested = sum(h.total_invested for h in industry_hlds)
            industry_total_gain_loss = sum(h.total_gain_loss for h in industry_hlds)
            industry_allocation = (
                (industry_total_invested / portfolio_total_invested * 100)
                if portfolio_total_invested > 0
                else 0.0
            )

            industry_perf = PortfolioIndustryPerformanceRead(
                industry=industry,
                currency="USD",
                total_invested=industry_total_invested,
                total_gain_loss=industry_total_gain_loss,
                allocation_percentage=industry_allocation,
            )
            industry_performances.append(industry_perf)

        return industry_performances
