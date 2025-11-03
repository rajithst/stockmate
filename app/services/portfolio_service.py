"""Portfolio service for managing user portfolios and trading activities."""

import logging

from sqlalchemy.orm import Session

from app.repositories.portfolio_repo import (
    PortfolioHoldingPerformanceRepository,
    PortfolioRepository,
    PortfolioTradingHistoryRepository,
)
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioHoldingPerformanceWrite,
    PortfolioRead,
    PortfolioTradingHistoryRead,
    PortfolioTradingHistoryWrite,
    PortfolioWrite,
)

logger = logging.getLogger(__name__)


class PortfolioService:
    """Service for managing portfolios and portfolio data."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._portfolio_repo = PortfolioRepository(session)
        self._holding_repo = PortfolioHoldingPerformanceRepository(session)
        self._trading_repo = PortfolioTradingHistoryRepository(session)

    def get_all_portfolios(self, user_id: int) -> list[PortfolioRead]:
        """Get all portfolios for a user."""
        portfolios = self._portfolio_repo.get_all_portfolios(user_id)
        return [PortfolioRead.model_validate(p) for p in portfolios]

    def upsert_portfolio(
        self, portfolio_in: PortfolioWrite, user_id: int
    ) -> PortfolioRead:
        """Create or update a portfolio for a user."""
        # Convert client model to internal model with user_id
        portfolio_data = portfolio_in.model_dump()
        portfolio_data["user_id"] = user_id
        portfolio_create = PortfolioCreate.model_validate(portfolio_data)
        portfolio = self._portfolio_repo.upsert_portfolio(portfolio_create)
        logger.info(f"Upserted portfolio {portfolio.id} for user {user_id}")
        return PortfolioRead.model_validate(portfolio)

    def delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        """Delete a portfolio (soft delete), ensuring it belongs to the authenticated user."""
        success = self._portfolio_repo.soft_delete_portfolio(portfolio_id, user_id)
        if success:
            logger.info(f"Deleted portfolio {portfolio_id} for user {user_id}")
        return success

    def buy_holding(
        self,
        trading: PortfolioTradingHistoryWrite,
        user_id: int,
    ) -> PortfolioTradingHistoryRead:
        """Record a buy transaction."""
        # Verify portfolio ownership
        if not self._portfolio_repo.verify_portfolio_ownership(
            trading.portfolio_id, user_id
        ):
            raise ValueError(f"Portfolio {trading.portfolio_id} not found")

        # Calculate totals
        total_value = trading.shares * trading.price_per_share
        net_total = total_value + trading.commission + trading.fees + trading.tax
        trade = trading.model_copy(
            update={"total_value": total_value, "net_total": net_total}
        )

        # insert to portfolio trading history
        self._trading_repo.add_trade(trade)
        logger.info(
            f"Recorded BUY trade: {trading.shares} shares of {trading.symbol} at ${trading.price_per_share} in portfolio {trading.portfolio_id}"
        )

        # insert to portfolio holding performance
        holding = self._holding_repo.get_holding(trading.portfolio_id, trading.symbol)
        if not holding:
            holding = PortfolioHoldingPerformanceWrite(
                portfolio_id=trading.portfolio_id,
                holding_symbol=trading.symbol,
                currency=trading.currency,
            )
            self._holding_repo.add_holding(holding)
        return trade

    def sell_holding(
        self,
        trading: PortfolioTradingHistoryWrite,
        user_id: int,
    ) -> PortfolioTradingHistoryWrite:
        """Record a sell transaction."""
        # Verify portfolio ownership
        if not self._portfolio_repo.verify_portfolio_ownership(
            trading.portfolio_id, user_id
        ):
            raise ValueError(f"Portfolio {trading.portfolio_id} not found")

        # Verify sufficient shares
        holding = self._holding_repo.get_holding(trading.portfolio_id, trading.symbol)
        if not holding:
            raise ValueError(
                f"No holding of {trading.symbol} exists in portfolio {trading.portfolio_id}"
            )

        if holding.total_shares < trading.shares:
            raise ValueError(
                f"Insufficient shares to sell. Have {holding.total_shares}, trying to sell {trading.shares}"
            )

        # Calculate totals
        total_value = trading.shares * trading.price_per_share
        net_total = total_value - trading.commission - trading.fees - trading.tax
        trade = trading.model_copy(
            update={"total_value": total_value, "net_total": net_total}
        )

        # insert to portfolio trading history
        self._trading_repo.add_trade(trade)
        logger.info(
            f"Recorded SELL trade: {trading.shares} shares of {trading.symbol} at ${trading.price_per_share} in portfolio {trading.portfolio_id}"
        )

        # update holding performance
        if holding.total_shares == trading.shares:
            # If all shares sold, remove holding
            self._holding_repo.delete_holding(holding.id)
            logger.info(
                f"Removed holding {trading.symbol} from portfolio {trading.portfolio_id} after selling all shares"
            )
        return trade
