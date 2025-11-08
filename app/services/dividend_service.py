"""Dividend sync service for calculating and storing portfolio dividends."""

import logging
from datetime import date as date_type

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.portfolio import PortfolioTradingHistory
from app.repositories.dividend_repo import CompanyDividendRepository
from app.repositories.portfolio_repo import (
    PortfolioDividendHistoryRepository,
    PortfolioRepository,
    PortfolioTradingHistoryRepository,
)
from app.schemas.user import PortfolioDividendHistoryWrite

logger = logging.getLogger(__name__)


class DividendSyncService:
    """Service for syncing company dividends to portfolio dividend history."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._dividend_repo = CompanyDividendRepository(session)
        self._portfolio_dividend_repo = PortfolioDividendHistoryRepository(session)
        self._portfolio_repo = PortfolioRepository(session)
        self._trading_repo = PortfolioTradingHistoryRepository(session)

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
    ) -> dict:
        """
        Sync dividends for a specific portfolio.

        Args:
            portfolio_id: The portfolio to sync dividends for
            after_date: Optional date to only process dividends after this date

        Returns:
            Dictionary with summary of processed dividends
        """
        # Get all unprocessed company dividends
        unprocessed_dividends = self._dividend_repo.get_unprocessed_dividends(
            after_date
        )

        processed_count = 0
        skipped_count = 0
        total_dividend_amount = 0.0
        processed_symbols = set()

        for company_dividend in unprocessed_dividends:
            symbol = company_dividend.symbol
            declaration_date = company_dividend.declaration_date
            payment_date = company_dividend.payment_date
            dividend_per_share = (
                company_dividend.adj_dividend or company_dividend.dividend
            )

            if not dividend_per_share or dividend_per_share <= 0:
                logger.warning(
                    f"Skipping dividend for {symbol} on {declaration_date}: "
                    "Invalid dividend amount"
                )
                skipped_count += 1
                continue

            # Check if already processed for this portfolio
            if self._portfolio_dividend_repo.dividend_exists(
                portfolio_id, symbol, payment_date
            ):
                logger.debug(
                    f"Dividend already processed for portfolio {portfolio_id}, "
                    f"symbol {symbol}, payment_date {payment_date}"
                )
                skipped_count += 1
                continue

            # Get all trades for this symbol before declaration date
            trades = self._trading_repo.get_trades_for_symbol_before_date(
                portfolio_id, symbol, declaration_date
            )

            if not trades:
                logger.debug(
                    f"No trades found for {symbol} before {declaration_date} "
                    f"in portfolio {portfolio_id}"
                )
                skipped_count += 1
                continue

            # Calculate shares held at declaration date
            shares_held = self._calculate_shares_held(trades)

            if shares_held <= 0:
                logger.debug(
                    f"No shares held for {symbol} at {declaration_date} "
                    f"in portfolio {portfolio_id}"
                )
                skipped_count += 1
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
            )
            self._portfolio_dividend_repo.record_dividend(dividend_record)

            processed_count += 1
            processed_symbols.add(symbol)
            total_dividend_amount += shares_held * dividend_per_share

        logger.info(
            f"Dividend sync for portfolio {portfolio_id}: "
            f"processed={processed_count}, skipped={skipped_count}, "
            f"total=${total_dividend_amount:.2f}"
        )

        return {
            "portfolio_id": portfolio_id,
            "processed_count": processed_count,
            "skipped_count": skipped_count,
            "total_dividend_amount": total_dividend_amount,
            "processed_symbols": list(processed_symbols),
        }

    def sync_all_portfolios(self, after_date: date_type | None = None) -> dict:
        """
        Sync dividends for all user portfolios.

        Args:
            after_date: Optional date to only process dividends after this date

        Returns:
            Dictionary with summary of all processed dividends
        """
        # Get all active portfolios
        stmt = select(PortfolioTradingHistory.portfolio_id).distinct()
        result = self._session.execute(stmt)
        portfolio_ids = [row[0] for row in result]

        total_processed = 0
        total_skipped = 0
        total_dividend_amount = 0.0
        portfolio_results = []

        for portfolio_id in portfolio_ids:
            result = self.sync_dividends_for_portfolio(portfolio_id, after_date)
            total_processed += result["processed_count"]
            total_skipped += result["skipped_count"]
            total_dividend_amount += result["total_dividend_amount"]
            portfolio_results.append(result)

        logger.info(
            f"Dividend sync for all portfolios: "
            f"total_processed={total_processed}, total_skipped={total_skipped}, "
            f"total=${total_dividend_amount:.2f}"
        )

        return {
            "total_processed": total_processed,
            "total_skipped": total_skipped,
            "total_dividend_amount": total_dividend_amount,
            "portfolio_results": portfolio_results,
        }
