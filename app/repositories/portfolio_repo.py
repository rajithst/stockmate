"""Portfolio repository for managing portfolio data access."""

import logging
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.portfolio import (
    Portfolio,
    PortfolioDividendHistory,
    PortfolioHoldingPerformance,
    PortfolioTradingHistory,
)
from app.db.models.quote import CompanyStockPrice
from app.schemas.user import (
    PortfolioCreate,
    PortfolioDividendHistoryWrite,
    PortfolioHoldingPerformanceWrite,
    PortfolioTradingHistoryWrite,
    PortfolioUpdate,
)
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class PortfolioRepository:
    """Repository for Portfolio operations."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def verify_portfolio_ownership(self, portfolio_id: int, user_id: int) -> bool:
        """Verify that a portfolio belongs to a specific user."""
        portfolio = (
            self._db.query(Portfolio)
            .filter_by(id=portfolio_id, user_id=user_id, deleted_at=None)
            .first()
        )
        return portfolio is not None

    def get_all_portfolios(self, user_id: int) -> list[Portfolio]:
        """
        Get all portfolios for a user (lightweight).

        Returns only basic portfolio info (id, name, description, currency, created_at, updated_at).
        Relations are NOT loaded to avoid unnecessary queries for list endpoints.

        Use get_portfolio_with_relations() if you need detailed portfolio data.
        """
        from sqlalchemy.orm import lazyload

        # Direct query overriding lazy="selectin" to prevent relation loading
        stmt = (
            select(Portfolio)
            .where((Portfolio.user_id == user_id) & (Portfolio.deleted_at.is_(None)))
            .options(
                lazyload(Portfolio.holding_performances),
                lazyload(Portfolio.trading_histories),
                lazyload(Portfolio.dividend_histories),
            )
        )
        return self._db.execute(stmt).scalars().all()

    def get_portfolio_by_id(self, portfolio_id: int) -> Portfolio | None:
        """Get a portfolio by its ID."""
        return (
            self._db.query(Portfolio)
            .filter_by(id=portfolio_id, deleted_at=None)
            .first()
        )

    def get_portfolio_with_relations(
        self, portfolio_id: int, user_id: int | None = None
    ) -> Portfolio | None:
        """
        Get a portfolio with all relations loaded and prices pre-cached.

        Args:
            portfolio_id: The portfolio ID to fetch
            user_id: Optional user ID to verify ownership

        Relations are auto-loaded via model's lazy="selectin" configuration.
        Prices are pre-loaded and cached to avoid future DB queries.

        Returns Portfolio with all relations + prices pre-loaded and cached.
        """
        # Build filter conditions
        filters = {"id": portfolio_id, "deleted_at": None}
        if user_id is not None:
            filters["user_id"] = user_id

        # Query portfolio - model's lazy="selectin" auto-loads all relations
        portfolio = self._db.query(Portfolio).filter_by(**filters).first()

        # Immediately pre-load and cache prices for all holdings
        if portfolio and portfolio.holding_performances:
            prices = self._load_current_prices_for_holdings(
                portfolio.holding_performances
            )
            for holding in portfolio.holding_performances:
                price = prices.get(holding.symbol, 0.0)
                holding.set_current_price(price)

        return portfolio

    def create_portfolio(self, portfolio_in: PortfolioCreate) -> Portfolio:
        """Create a new portfolio."""
        portfolio = Portfolio(**portfolio_in.model_dump(exclude_unset=True))
        self._db.add(portfolio)
        self._db.commit()
        self._db.refresh(portfolio)
        logger.info(f"Created portfolio {portfolio.id} for user {portfolio.user_id}")
        return portfolio

    def update_portfolio(self, portfolio_in: PortfolioUpdate) -> Portfolio:
        """Update an existing portfolio."""
        portfolio = (
            self._db.query(Portfolio)
            .filter_by(id=portfolio_in.id, user_id=portfolio_in.user_id)
            .first()
        )

        if not portfolio:
            logger.warning(f"Portfolio {portfolio_in.id} not found")
            return None

        # Map fields from schema to model
        map_model(portfolio, portfolio_in)
        self._db.commit()
        self._db.refresh(portfolio)
        logger.info(f"Updated portfolio {portfolio.id}")
        return portfolio

    def soft_delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        """Soft delete a portfolio."""
        portfolio = (
            self._db.query(Portfolio)
            .filter_by(id=portfolio_id, user_id=user_id, deleted_at=None)
            .first()
        )

        if not portfolio:
            logger.warning(f"Portfolio {portfolio_id} not found for user {user_id}")
            return False

        portfolio.deleted_at = datetime.now(timezone.utc)
        self._db.commit()
        logger.info(f"Soft deleted portfolio {portfolio_id}")
        return True

    def _load_current_prices_for_holdings(
        self, holdings: list[PortfolioHoldingPerformance]
    ) -> dict[str, float]:
        """
        Bulk load latest prices for all holdings in a single query.

        Returns a dict mapping symbol -> current_price
        """
        if not holdings:
            return {}

        symbols = list({holding.symbol for holding in holdings})

        # Single query: get latest price for each symbol using window function
        # Subquery to rank prices by date (most recent first)
        subquery = (
            select(
                CompanyStockPrice.symbol,
                CompanyStockPrice.close_price,
                func.row_number()
                .over(
                    partition_by=CompanyStockPrice.symbol,
                    order_by=CompanyStockPrice.date.desc(),
                )
                .label("rn"),
            )
            .where(CompanyStockPrice.symbol.in_(symbols))
            .subquery()
        )

        # Get only the latest price for each symbol (rn = 1)
        stmt = select(subquery.c.symbol, subquery.c.close_price).where(
            subquery.c.rn == 1
        )

        results = self._db.execute(stmt).all()
        prices = {row[0]: row[1] for row in results}

        # Fill in missing symbols with 0.0
        for symbol in symbols:
            if symbol not in prices:
                prices[symbol] = 0.0

        return prices


class PortfolioHoldingPerformanceRepository:
    """Repository for PortfolioHoldingPerformance operations."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def get_holding(
        self, portfolio_id: int, symbol: str
    ) -> PortfolioHoldingPerformance | None:
        """Get a specific holding by portfolio and symbol."""
        return (
            self._db.query(PortfolioHoldingPerformance)
            .filter_by(portfolio_id=portfolio_id, symbol=symbol)
            .first()
        )

    def add_holding(
        self, holding_in: PortfolioHoldingPerformanceWrite
    ) -> PortfolioHoldingPerformance:
        """Add or update a holding in the portfolio."""
        # Find existing holding
        existing = (
            self._db.query(PortfolioHoldingPerformance)
            .filter_by(portfolio_id=holding_in.portfolio_id, symbol=holding_in.symbol)
            .first()
        )

        if existing:
            # Update existing
            map_model(existing, holding_in)
            holding = existing
        else:
            # Create new
            holding = PortfolioHoldingPerformance(
                **holding_in.model_dump(exclude_unset=True)
            )
            self._db.add(holding)

        self._db.commit()
        self._db.refresh(holding)
        logger.info(
            f"Added/Updated holding {holding.symbol} in portfolio {holding.portfolio_id}"
        )
        return holding

    def delete_holding(self, holding_id: int) -> bool:
        """Delete a holding from the portfolio by ID."""
        holding = (
            self._db.query(PortfolioHoldingPerformance).filter_by(id=holding_id).first()
        )

        if not holding:
            logger.warning(f"Holding {holding_id} not found")
            return False

        self._db.delete(holding)
        self._db.commit()
        logger.info(f"Deleted holding {holding_id}")
        return True


class PortfolioTradingHistoryRepository:
    """Repository for PortfolioTradingHistory operations."""

    def __init__(self, session: Session) -> None:
        self._db = session

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
        trade = PortfolioTradingHistory(**trade_in.model_dump(exclude_unset=True))
        self._db.add(trade)
        self._db.commit()
        self._db.refresh(trade)
        logger.info(
            f"Added {trade.trade_type} trade for {trade.symbol} in portfolio {trade.portfolio_id}"
        )
        return trade


class PortfolioDividendHistoryRepository:
    """Repository for PortfolioDividendHistory operations."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def get_dividend_history_by_portfolio(
        self, portfolio_id: int
    ) -> list[PortfolioDividendHistory]:
        """Get all dividend history for a portfolio."""
        return (
            self._db.query(PortfolioDividendHistory)
            .filter_by(portfolio_id=portfolio_id)
            .all()
        )

    def record_dividend(
        self, dividend_record: PortfolioDividendHistoryWrite
    ) -> PortfolioDividendHistory:
        """Record a dividend for a portfolio holding."""
        # Find existing dividend record
        existing = (
            self._db.query(PortfolioDividendHistory)
            .filter_by(
                portfolio_id=dividend_record.portfolio_id,
                symbol=dividend_record.symbol,
                payment_date=dividend_record.payment_date,
            )
            .first()
        )

        if existing:
            # Update existing
            map_model(existing, dividend_record)
            record = existing
        else:
            # Create new
            record = PortfolioDividendHistory(
                **dividend_record.model_dump(exclude_unset=True)
            )
            self._db.add(record)

        self._db.commit()
        self._db.refresh(record)
        logger.info(
            f"Recorded dividend for {record.symbol} in portfolio {record.portfolio_id}"
        )
        return record
