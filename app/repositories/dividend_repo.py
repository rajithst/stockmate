"""Dividend repository for managing dividend data access."""

import logging
from datetime import date as date_type

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.db.models.dividend import CompanyDividend
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class CompanyDividendRepository(BaseRepository[CompanyDividend]):
    """Repository for CompanyDividend operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_dividend_by_symbol_date(
        self, symbol: str, dividend_date: date_type
    ) -> CompanyDividend | None:
        """Get a dividend by symbol and ex-dividend date."""
        stmt = select(CompanyDividend).where(
            and_(
                CompanyDividend.symbol == symbol, CompanyDividend.date == dividend_date
            )
        )
        result = self._db.execute(stmt).first()
        return result[0] if result else None

    def get_unprocessed_dividends(
        self, after_date: date_type | None = None
    ) -> list[CompanyDividend]:
        """Get all company dividends that haven't been processed yet."""
        # Unprocessed means: has declaration_date and payment_date but not processed yet
        stmt = select(CompanyDividend).where(
            and_(
                CompanyDividend.declaration_date.is_not(None),
                CompanyDividend.payment_date.is_not(None),
            )
        )
        if after_date:
            stmt = stmt.where(CompanyDividend.declaration_date >= after_date)

        # Order by declaration date to process chronologically
        stmt = stmt.order_by(CompanyDividend.declaration_date)
        return self._db.execute(stmt).scalars().all()

    def get_dividends_by_symbol(self, symbol: str) -> list[CompanyDividend]:
        """Get all dividends for a specific stock symbol."""
        stmt = (
            select(CompanyDividend)
            .where(CompanyDividend.symbol == symbol)
            .order_by(CompanyDividend.date.desc())
        )
        return self._db.execute(stmt).scalars().all()

    def get_dividends_by_date_range(
        self, start_date: date_type, end_date: date_type
    ) -> list[CompanyDividend]:
        """Get all dividends within a date range (by declaration date)."""
        stmt = (
            select(CompanyDividend)
            .where(
                and_(
                    CompanyDividend.declaration_date >= start_date,
                    CompanyDividend.declaration_date <= end_date,
                )
            )
            .order_by(CompanyDividend.declaration_date)
        )
        return self._db.execute(stmt).scalars().all()
