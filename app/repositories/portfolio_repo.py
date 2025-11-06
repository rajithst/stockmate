"""Portfolio repository for managing portfolio data access."""

import logging
from datetime import datetime, timezone

from sqlalchemy import func as sql_func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.company import Company
from app.db.models.portfolio import (
    Portfolio,
    PortfolioDividendHistory,
    PortfolioHoldingPerformance,
    PortfolioTradingHistory,
)
from app.db.models.quote import StockPrice
from app.repositories.base_repo import BaseRepository
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioDividendHistoryWrite,
    PortfolioHoldingPerformanceWrite,
    PortfolioTradingHistoryWrite,
    PortfolioUpdate,
)

logger = logging.getLogger(__name__)


class PortfolioRepository(BaseRepository[Portfolio]):
    """Repository for Portfolio operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def verify_portfolio_ownership(self, portfolio_id: int, user_id: int) -> bool:
        """Verify that a portfolio belongs to a specific user."""
        portfolios = self._get_by_filter(
            Portfolio, {"id": portfolio_id, "user_id": user_id, "deleted_at": None}
        )
        return len(portfolios) > 0

    def get_all_portfolios(self, user_id: int) -> list[Portfolio]:
        """Get all portfolios for a user."""
        return self._get_by_filter(Portfolio, {"user_id": user_id, "deleted_at": None})

    def get_portfolio_by_id(self, portfolio_id: int) -> Portfolio | None:
        """Get a portfolio by its ID."""
        portfolios = self._get_by_filter(
            Portfolio, {"id": portfolio_id, "deleted_at": None}
        )
        return portfolios[0] if portfolios else None

    def create_portfolio(
        self,
        portfolio_in: PortfolioCreate,
    ) -> Portfolio:
        """Create a new portfolio."""
        return self._upsert_single(
            portfolio_in, Portfolio, lambda p: {"id": None}, "create_portfolio"
        )

    def update_portfolio(
        self,
        portfolio_in: PortfolioUpdate,
    ) -> Portfolio:
        """Update an existing portfolio."""
        return self._upsert_single(
            portfolio_in,
            Portfolio,
            lambda p: {"id": p.id, "user_id": p.user_id},
            "update_portfolio",
        )

    def soft_delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        """Soft delete a portfolio."""
        portfolio = self._get_by_filter(
            Portfolio, {"id": portfolio_id, "user_id": user_id, "deleted_at": None}
        )
        if not portfolio:
            logger.warning(f"Portfolio {portfolio_id} not found for user {user_id}")
            return False

        portfolio.deleted_at = datetime.now(timezone.utc)
        self._db.commit()
        logger.info(f"Soft deleted portfolio {portfolio_id}")
        return True


class PortfolioHoldingPerformanceRepository(
    BaseRepository[PortfolioHoldingPerformance]
):
    """Repository for PortfolioHoldingPerformance operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_holdings_by_portfolio(
        self, portfolio_id: int
    ) -> list[PortfolioHoldingPerformance]:
        """Get all holdings for a portfolio."""
        return self._get_by_filter(
            PortfolioHoldingPerformance, {"portfolio_id": portfolio_id}
        )

    def get_holding(
        self, portfolio_id: int, symbol: str
    ) -> PortfolioHoldingPerformance | None:
        """Get a specific holding by portfolio and symbol."""
        holdings = self._get_by_filter(
            PortfolioHoldingPerformance,
            {"portfolio_id": portfolio_id, "symbol": symbol},
        )
        return holdings[0] if holdings else None

    def add_holding(
        self, holding_in: PortfolioHoldingPerformanceWrite
    ) -> PortfolioHoldingPerformance:
        """Add or update a holding in the portfolio."""
        holding = self._upsert_single(
            holding_in,
            PortfolioHoldingPerformance,
            lambda h: {"portfolio_id": h.portfolio_id, "symbol": h.symbol},
            "add_holding",
        )
        logger.info(
            f"Added/Updated holding {holding.symbol} in portfolio {holding.portfolio_id}"
        )
        return holding

    def delete_holding(self, holding_id: int) -> bool:
        """Delete a holding from the portfolio by ID."""
        holding = (
            self._db.query(PortfolioHoldingPerformance)
            .filter(PortfolioHoldingPerformance.id == holding_id)
            .first()
        )
        if not holding:
            logger.warning(f"Holding {holding_id} not found")
            return False
        self._db.delete(holding)
        self._db.commit()
        logger.info(f"Deleted holding {holding_id}")
        return True

    def load_current_prices_for_holdings(
        self, holdings: list[PortfolioHoldingPerformance]
    ) -> dict[str, float]:
        """
        Bulk load current prices for all holdings to avoid N+1 queries.

        Returns a dict mapping symbol -> current_price
        """

        if not holdings:
            return {}

        symbols = list({holding.symbol for holding in holdings})

        # Get the most recent price for each symbol in a single query
        stmt = (
            select(
                StockPrice.symbol, sql_func.max(StockPrice.date).label("latest_date")
            )
            .where(StockPrice.symbol.in_(symbols))
            .group_by(StockPrice.symbol)
        )

        latest_dates = {row[0]: row[1] for row in self._db.execute(stmt).all()}

        if not latest_dates:
            return {symbol: 0.0 for symbol in symbols}

        # Get the prices for those latest dates
        stmt = select(StockPrice).where(
            (StockPrice.symbol.in_(symbols))
            & (
                (StockPrice.symbol == StockPrice.symbol)
                & (StockPrice.date.in_(latest_dates.values()))
            )
        )

        results = self._db.execute(stmt).scalars().all()
        prices = {result.symbol: result.close_price for result in results}

        # Fill in missing symbols with 0.0
        for symbol in symbols:
            if symbol not in prices:
                prices[symbol] = 0.0

        return prices

    def load_company_sectors_for_holdings(
        self, holdings: list[PortfolioHoldingPerformance]
    ) -> dict[str, str]:
        """
        Bulk load company sectors for all holdings to avoid N+1 queries.

        Returns a dict mapping symbol -> sector
        """

        if not holdings:
            return {}

        symbols = list({holding.symbol for holding in holdings})

        # Get all companies for these symbols in a single query
        stmt = select(Company).where(Company.symbol.in_(symbols))
        companies = self._db.execute(stmt).scalars().all()

        sectors_map = {company.symbol: company.sector for company in companies}

        # Fill in missing symbols with empty string
        for symbol in symbols:
            if symbol not in sectors_map:
                sectors_map[symbol] = ""

        return sectors_map

    def load_company_industries_for_holdings(
        self, holdings: list[PortfolioHoldingPerformance]
    ) -> dict[str, str]:
        """
        Bulk load company industries for all holdings to avoid N+1 queries.

        Returns a dict mapping symbol -> industry
        """

        if not holdings:
            return {}

        symbols = list({holding.symbol for holding in holdings})

        # Get all companies for these symbols in a single query
        stmt = select(Company).where(Company.symbol.in_(symbols))
        companies = self._db.execute(stmt).scalars().all()

        industries_map = {company.symbol: company.industry for company in companies}

        # Fill in missing symbols with empty string
        for symbol in symbols:
            if symbol not in industries_map:
                industries_map[symbol] = ""

        return industries_map


class PortfolioTradingHistoryRepository(BaseRepository[PortfolioTradingHistory]):
    """Repository for PortfolioTradingHistory operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_trading_history_by_portfolio(
        self, portfolio_id: int
    ) -> list[PortfolioTradingHistory]:
        """Get all trading history for a portfolio."""
        return self._get_by_filter(
            PortfolioTradingHistory, {"portfolio_id": portfolio_id}
        )

    def get_trades_for_symbol_before_date(
        self, portfolio_id: int, symbol: str, before_date
    ) -> list[PortfolioTradingHistory]:
        """Get all trades for a symbol before a specific date."""
        stmt = select(PortfolioTradingHistory).where(
            (PortfolioTradingHistory.portfolio_id == portfolio_id)
            & (PortfolioTradingHistory.symbol == symbol)
            & (PortfolioTradingHistory.trade_date < before_date)
        )
        return self._db.execute(stmt).scalars().all()

    def add_trade(
        self, trade_in: PortfolioTradingHistoryWrite
    ) -> PortfolioTradingHistory:
        """Add a buy or sell trade to the trading history."""
        trade = self._upsert_single(
            trade_in,
            PortfolioTradingHistory,
            lambda h: {"id": None},
            operation_name="add_trade",
        )
        logger.info(
            f"Added {trade.trade_type} trade for {trade.symbol} in portfolio {trade.portfolio_id}"
        )
        return trade


class PortfolioDividendHistoryRepository(BaseRepository[PortfolioDividendHistory]):
    """Repository for PortfolioDividendHistory operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_dividend_history_by_portfolio(
        self, portfolio_id: int
    ) -> list[PortfolioDividendHistory]:
        """Get all dividend history for a portfolio."""
        return self._get_by_filter(
            PortfolioDividendHistory, {"portfolio_id": portfolio_id}
        )

    def record_dividend(
        self, dividend_record: PortfolioDividendHistoryWrite
    ) -> PortfolioDividendHistory:
        """Record a dividend for a portfolio holding."""
        return self._upsert_single(
            dividend_record,
            PortfolioDividendHistory,
            lambda d: {
                "portfolio_id": d.portfolio_id,
                "symbol": d.symbol,
                "payment_date": d.payment_date,
            },
            "record_dividend",
        )

    def dividend_exists(self, portfolio_id: int, symbol: str, payment_date) -> bool:
        """Check if a dividend record already exists for this portfolio/symbol/date."""
        stmt = select(PortfolioDividendHistory).where(
            (PortfolioDividendHistory.portfolio_id == portfolio_id)
            & (PortfolioDividendHistory.symbol == symbol)
            & (PortfolioDividendHistory.payment_date == payment_date)
        )
        result = self._db.execute(stmt).first()
        return result is not None
