"""Portfolio repository for managing portfolio data access."""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.portfolio import (
    Portfolio,
    PortfolioTradingHistory,
)
from app.repositories.base_repo import BaseRepository
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioHoldingPerformance,
    PortfolioHoldingPerformanceWrite,
    PortfolioTradingHistoryWrite,
)

logger = logging.getLogger(__name__)


class PortfolioRepository(BaseRepository[Portfolio]):
    """Repository for Portfolio operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def verify_portfolio_ownership(self, portfolio_id: int, user_id: int) -> bool:
        """Verify that a portfolio belongs to a specific user."""
        portfolio = self._get_by_filter(
            Portfolio, {"id": portfolio_id, "user_id": user_id, "deleted_at": None}
        )
        return portfolio is not None

    def get_all_portfolios(self, user_id: int) -> list[Portfolio]:
        """Get all portfolios for a user."""
        return self._get_by_filter(Portfolio, {"user_id": user_id, "deleted_at": None})

    def upsert_portfolio(
        self,
        portfolio_in: PortfolioCreate,
    ) -> Portfolio:
        """Create a new portfolio."""
        return self._upsert_single(
            portfolio_in,
            Portfolio,
            lambda p: {"id": p.id, "user_id": p.user_id, "name": p.name},
            "create_portfolio",
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

    def add_holding(
        self, holding_in: PortfolioHoldingPerformanceWrite
    ) -> PortfolioHoldingPerformance:
        """Add or update a holding in the portfolio."""
        holding = self._upsert_single(
            holding_in,
            PortfolioHoldingPerformance,
            lambda h: {
                "portfolio_id": h.portfolio_id,
                "holding_symbol": h.holding_symbol,
                "currency": h.currency,
            },
            "add_holding",
        )
        logger.info(
            f"Added/Updated holding {holding.holding_symbol} in portfolio {holding.portfolio_id}"
        )
        return holding

    def delete_holding(self, portfolio_id: int, holding_symbol: str) -> bool:
        """Delete a holding from the portfolio."""
        return self._delete_by_filter(
            PortfolioHoldingPerformance,
            {"portfolio_id": portfolio_id, "holding_symbol": holding_symbol},
            "delete_holding",
        )


class PortfolioTradingHistoryRepository(BaseRepository[PortfolioTradingHistory]):
    """Repository for PortfolioTradingHistory operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def add_trade(
        self, trade_in: PortfolioTradingHistoryWrite
    ) -> PortfolioTradingHistory:
        """Add a buy or sell trade to the trading history."""
        trade = self._insert_single(
            trade_in, PortfolioTradingHistory, operation_name="add_trade"
        )
        logger.info(
            f"Added {trade.trade_type} trade for {trade.symbol} in portfolio {trade.portfolio_id}"
        )
        return trade
