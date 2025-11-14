import logging

from sqlalchemy.orm import Session
from datetime import date as date_type

from app.repositories.portfolio_repo import (
    PortfolioRepository,
)
from app.schemas.user import (
    PortfolioCreate,
    PortfolioDetail,
    PortfolioDividendHistoryRead,
    PortfolioDividendHistoryWrite,
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

    @staticmethod
    def _validate_list(items: list, schema_class):
        """Convert list of items to validated schema instances."""
        return [schema_class.model_validate(item) for item in items]

    def _get_verified_portfolio(self, portfolio_id: int, user_id: int):
        """Get portfolio and verify ownership, raising ValueError if not found or unauthorized."""
        portfolio = self._portfolio_repo.get_portfolio_by_id(portfolio_id)
        if (
            not portfolio
            or portfolio.user_id != user_id
            or portfolio.deleted_at is not None
        ):
            raise ValueError("Portfolio not found or access denied")
        return portfolio

    def get_all_portfolios(self, user_id: int) -> list[PortfolioRead]:
        """
        Get all portfolios for a user with calculated totals.

        Relations are NOT loaded during query (lightweight), but totals are computed
        from pre-loaded data without triggering additional database queries.

        For detailed portfolio data with holdings trades, and dividends,
        use get_portfolio_details() instead.
        """
        portfolios = self._portfolio_repo.get_all_portfolios(user_id)
        return [
            PortfolioRead(
                id=p.id,
                name=p.name,
                description=p.description,
                currency=p.currency,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in portfolios
        ]

    def create_portfolio(
        self, portfolio_in: PortfolioUpsertRequest, user_id: int
    ) -> PortfolioRead:
        """Create a new portfolio for a user."""
        portfolio_create = PortfolioCreate(
            name=portfolio_in.name,
            description=portfolio_in.description,
            currency=portfolio_in.currency,
            user_id=user_id,
        )
        portfolio_dto = self._portfolio_repo.create_portfolio(portfolio_create)
        logger.info(f"Created portfolio {portfolio_dto.id} for user {user_id}")
        return PortfolioRead(
            id=portfolio_dto.id,
            name=portfolio_dto.name,
            description=portfolio_dto.description,
            currency=portfolio_dto.currency,
            created_at=portfolio_dto.created_at,
            updated_at=portfolio_dto.updated_at,
        )

    def update_portfolio(
        self, portfolio_id: int, portfolio_in: PortfolioUpsertRequest, user_id: int
    ) -> PortfolioRead:
        """Update an existing portfolio for a user."""
        portfolio = self._get_verified_portfolio(portfolio_id, user_id)

        portfolio_update = PortfolioUpdate(
            id=portfolio.id,
            user_id=portfolio.user_id,
            name=portfolio_in.name,
            description=portfolio_in.description,
            currency=portfolio_in.currency,
        )
        updated_dto = self._portfolio_repo.update_portfolio(portfolio_update)
        logger.info(f"Updated portfolio {updated_dto.id} for user {user_id}")
        return PortfolioRead(
            id=updated_dto.id,
            name=updated_dto.name,
            description=updated_dto.description,
            currency=updated_dto.currency,
            created_at=updated_dto.created_at,
            updated_at=updated_dto.updated_at,
        )

    def delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        """Delete a portfolio (soft delete), ensuring it belongs to the authenticated user."""
        self._get_verified_portfolio(portfolio_id, user_id)

        success = self._portfolio_repo.soft_delete_portfolio(portfolio_id, user_id)
        if success:
            logger.info(f"Deleted portfolio {portfolio_id} for user {user_id}")
        return success

    def get_portfolio_details(self, portfolio_id: int, user_id: int) -> PortfolioDetail:
        """
        Get detailed portfolio information including holdings, trading history, and dividends.
        Args:
            portfolio_id: The portfolio to retrieve details for
            user_id: The user requesting the portfolio details
        Returns:
            PortfolioDetail: Detailed portfolio information
        """
        # Fetch portfolio with all relations and verify ownership in one optimized call
        portfolio = self._portfolio_repo.get_portfolio_with_relations(
            portfolio_id, user_id
        )
        if not portfolio:
            raise ValueError("Portfolio not found or access denied")

        # Access relations - already loaded, no additional queries
        holdings = portfolio.holding_performances
        trading_history = portfolio.trading_histories
        dividends = portfolio.dividend_histories

        # Calculate total dividends received
        dividends_received = sum(d.dividend_amount for d in dividends)

        company_sectors = {h.symbol: h.sector for h in holdings}
        company_industries = {h.symbol: h.industry for h in holdings}

        # Calculate sector and industry performance on-the-fly
        sector_performances = self._calculate_sector_performances(
            holdings, company_sectors
        )
        industry_performances = self._calculate_industry_performances(
            holdings, company_industries
        )

        return PortfolioDetail(
            total_value=portfolio.total_value,
            total_invested=portfolio.total_invested,
            total_gain_loss=portfolio.total_gain_loss,
            dividends_received=dividends_received,
            total_return_percentage=portfolio.total_return_percentage,
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

    def get_portfolio_dividend_history(
        self, portfolio_id: int, user_id: int
    ) -> list[PortfolioDividendHistoryRead]:
        """
        Retrieve dividend history for a specific portfolio.

        Args:
            portfolio_id: The portfolio to retrieve dividend history for
            user_id: The user requesting the dividend history
        Returns:
            List of PortfolioDividendHistoryRead records
        """
        try:
            self._get_verified_portfolio(portfolio_id, user_id)
            dividend_histories = self._portfolio_repo.get_dividend_history(portfolio_id)
            results = self._validate_list(
                dividend_histories, PortfolioDividendHistoryRead
            )
            return results
        except Exception as e:
            logger.error(
                f"Error retrieving dividend history for portfolio {portfolio_id}: {str(e)}",
                exc_info=True,
            )
            raise

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
        response = self._portfolio_repo.add_trade(trade_write)
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
        holding = self._portfolio_repo.get_holding(portfolio_id, trading.symbol)
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
        response = self._portfolio_repo.add_trade(trade_write)
        logger.info(
            f"Recorded SELL trade: {trading.shares} shares of {trading.symbol} at ${trading.price_per_share} in portfolio {portfolio_id}"
        )

        # Remove holding if all shares sold
        if holding.total_shares == trading.shares:
            self._portfolio_repo.delete_holding(holding.id)
            logger.info(
                f"Removed holding {trading.symbol} from portfolio {portfolio_id} after selling all shares"
            )

        return PortfolioTradingHistoryRead.model_validate(response)

    def sync_dividends_for_portfolio(
        self, portfolio_id: int, after_date: date_type | None = None
    ) -> list[PortfolioDividendHistoryRead]:
        """
        Sync dividends for a specific portfolio.

        Args:
            portfolio_id: The portfolio to sync dividends for
            after_date: Optional date to only process dividends after this date

        Returns:
            Dictionary with summary of processed dividends
        """
        # Get all unprocessed company dividends
        try:
            unprocessed_dividends = self._dividend_repo.get_unprocessed_dividends(
                after_date
            )
            dividend_created = []

            for company_dividend in unprocessed_dividends:
                symbol = company_dividend.symbol
                declaration_date = company_dividend.declaration_date
                payment_date = company_dividend.payment_date
                dividend_per_share = (
                    company_dividend.adj_dividend or company_dividend.dividend
                )
                currency = company_dividend.currency

                if not dividend_per_share or dividend_per_share <= 0:
                    logger.warning(
                        f"Skipping dividend for {symbol} on {declaration_date}: "
                        "Invalid dividend amount"
                    )
                    continue

                # Get all trades for this symbol before declaration date
                trades = self._portfolio_repo.get_trading_history_before_date(
                    portfolio_id, symbol, declaration_date
                )

                if not trades:
                    logger.debug(
                        f"No trades found for {symbol} before {declaration_date} "
                        f"in portfolio {portfolio_id}"
                    )
                    continue

                # Calculate shares held at declaration date
                shares_held = self._calculate_shares_held(trades)

                if shares_held <= 0:
                    logger.debug(
                        f"No shares held for {symbol} at {declaration_date} "
                        f"in portfolio {portfolio_id}"
                    )
                    continue

                # Record the dividend
                dividend_record = PortfolioDividendHistoryWrite(
                    portfolio_id=portfolio_id,
                    symbol=symbol,
                    shares=shares_held,
                    dividend_per_share=dividend_per_share,
                    dividend_amount=shares_held * dividend_per_share,
                    declaration_date=declaration_date,
                    payment_date=payment_date,
                    currency=currency,
                )
                result = self._portfolio_repo.add_dividend(dividend_record)
                dividend_created.append(result)
            results = [
                PortfolioDividendHistoryRead.model_validate(dividend)
                for dividend in dividend_created
            ]
            return results
        except Exception as e:
            logger.error(
                f"Error syncing dividends for portfolio {portfolio_id}: {str(e)}",
                exc_info=True,
            )
            raise

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
        holding = self._portfolio_repo.get_holding(portfolio_id, symbol)
        if not holding:
            holding_write = PortfolioHoldingPerformanceWrite(
                portfolio_id=portfolio_id,
                symbol=symbol,
                currency=currency,
            )
            self._portfolio_repo.add_holding(holding_write)

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
