"""Dividend sync service for calculating and storing portfolio dividends."""

import logging
from datetime import date as date_type

from sqlalchemy.orm import Session

from app.repositories.portfolio_repo import (
    PortfolioRepository,
)
from app.schemas.user import PortfolioDividendHistoryRead, PortfolioDividendHistoryWrite
from app.db.models.portfolio import PortfolioTradingHistory

logger = logging.getLogger(__name__)


class DividendService:
    """Service for dividend calculations and syncing."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._portfolio_repo = PortfolioRepository(session)

    def _calculate_shares_held(self, trades: list[PortfolioTradingHistory]) -> float:
        """Calculate total shares held based on buy and sell trades."""
        shares_held = 0.0
        for trade in trades:
            if trade.trade_type == "BUY":
                shares_held += trade.shares
            elif trade.trade_type == "SELL":
                shares_held -= trade.shares
        return shares_held

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
            unprocessed_dividends = self._portfolio_repo.get_unprocessed_dividends(
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

    def sync_all_portfolios(
        self, after_date: date_type | None = None
    ) -> list[PortfolioDividendHistoryRead]:
        """
        Sync dividends for all user portfolios.

        Args:
            after_date: Optional date to only process dividends after this date

        Returns:
            Dictionary with summary of all processed dividends
        """
        # Get all active portfolios
        try:
            results = []
            portfolio_ids = self._portfolio_repo.get_all_portfolios()
            portfolio_ids = [p.id for p in portfolio_ids]

            for portfolio_id in portfolio_ids:
                result = self.sync_dividends_for_portfolio(portfolio_id, after_date)
                results.extend(result)
            return results
        except Exception as e:
            logger.error(
                f"Error syncing dividends for all portfolios: {str(e)}", exc_info=True
            )
            raise
