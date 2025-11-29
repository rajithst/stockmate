import logging

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models import CompanyStockPrice, CompanyEarningsCalendar, IndexQuote
from app.db.models.dividend import CompanyDividend
from app.db.models.stock import CompanyStockPeer, CompanyStockSplit
from app.db.models.technical_indicators import CompanyTechnicalIndicator

logger = logging.getLogger(__name__)


class CompanyQuotesRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_daily_prices(self, symbol: str, limit: int = 2000) -> list:
        """Retrieve daily price records for a company."""
        try:
            return (
                self._db.query(CompanyStockPrice)
                .filter(CompanyStockPrice.symbol == symbol)
                .order_by(CompanyStockPrice.date.desc())
                .limit(limit)
                .all()
            )
        except Exception as e:
            logger.error(f"Error retrieving daily prices for symbol {symbol}: {e}")
            return []

    def get_dividends(self, symbol: str, limit: int = 50) -> list[CompanyDividend]:
        """Retrieve dividend records for a company."""
        try:
            return (
                self._db.query(CompanyDividend)
                .filter(CompanyDividend.symbol == symbol)
                .order_by(CompanyDividend.date.desc())
                .limit(limit)
                .all()
            )
        except Exception as e:
            logger.error(f"Error retrieving dividends for symbol {symbol}: {e}")
            return []

    def get_stock_splits(self, symbol: str, limit: int = 50) -> list[CompanyStockSplit]:
        """Retrieve stock split records for a company."""
        try:
            return (
                self._db.query(CompanyStockSplit)
                .filter(CompanyStockSplit.symbol == symbol)
                .order_by(CompanyStockSplit.date.desc())
                .limit(limit)
                .all()
            )
        except Exception as e:
            logger.error(f"Error retrieving stock splits for symbol {symbol}: {e}")
            return []

    def get_stock_peers(self, symbol: str) -> list[CompanyStockPeer]:
        """Retrieve stock peers for a company."""
        try:
            return (
                self._db.query(CompanyStockPeer)
                .filter(CompanyStockPeer.symbol == symbol)
                .all()
            )
        except Exception as e:
            logger.error(f"Error retrieving stock peers for symbol {symbol}: {e}")
            return []

    def get_technical_indicators(self, symbol: str) -> list[CompanyTechnicalIndicator]:
        """Retrieve technical indicators for a company."""
        try:
            return (
                self._db.query(CompanyTechnicalIndicator)
                .filter(CompanyTechnicalIndicator.symbol == symbol)
                .order_by(CompanyTechnicalIndicator.date.desc())
                .all()
            )
        except Exception as e:
            logger.error(
                f"Error retrieving technical indicators for symbol {symbol}: {e}"
            )
            return []

    def get_index_quotes(self) -> list[IndexQuote]:
        """Retrieve index quotes."""
        try:
            return self._db.query(IndexQuote).all()
        except Exception as e:
            logger.error(f"Error retrieving index quotes: {e}")
            return []

    def get_earnings_calendar(
        self, from_date: str, to_date: str
    ) -> list[CompanyEarningsCalendar]:
        """Retrieve earnings calendar for companies within a date range.

        Filters by either date or last_update within the specified range.
        """
        try:
            return (
                self._db.query(CompanyEarningsCalendar)
                .filter(
                    or_(
                        (CompanyEarningsCalendar.date >= from_date)
                        & (CompanyEarningsCalendar.date <= to_date),
                        (CompanyEarningsCalendar.last_update >= from_date)
                        & (CompanyEarningsCalendar.last_update <= to_date),
                    )
                )
                .order_by(CompanyEarningsCalendar.date.asc())
                .all()
            )
        except Exception as e:
            logger.error(
                f"Error retrieving earnings calendar from {from_date} to {to_date}: {e}"
            )
            return []

    def get_dividend_calendar(
        self, from_date: str, to_date: str
    ) -> list[CompanyDividend]:
        """Retrieve dividend calendar for companies within a date range.

        Filters by either date or last_update within the specified range.
        """
        try:
            return (
                self._db.query(CompanyDividend)
                .filter(
                    CompanyDividend.date
                    >= from_date & CompanyEarningsCalendar.date
                    <= to_date
                )
                .order_by(CompanyDividend.date.asc())
                .all()
            )
        except Exception as e:
            logger.error(
                f"Error retrieving dividend calendar from {from_date} to {to_date}: {e}"
            )
            return []
