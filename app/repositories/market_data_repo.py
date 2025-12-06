import enum
import logging
from typing import TypeVar

from sqlalchemy.orm import Session

from app.db.models.grading import CompanyGrading, CompanyGradingSummary
from app.db.models.news import (
    News,
)
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)


class CompanyMarketDataRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_latest_news(
        self, from_date: str, to_date: str, limit: int = 1000
    ) -> list[News]:
        """Retrieve the latest news articles within a date range."""
        try:
            return (
                self._db.query(News)
                .filter(News.published_date >= from_date)
                .filter(News.published_date <= to_date)
                .order_by(News.published_date.desc())
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting latest news: {e}")
            raise

    def get_stock_news(
        self, symbol: str, from_date: str, to_date: str, limit: int = 1000
    ) -> list[News]:
        """Retrieve stock-specific news articles for a given symbol within a date range."""
        try:
            return (
                self._db.query(News)
                .filter(News.symbol == symbol)
                .filter(News.published_date >= from_date)
                .filter(News.published_date <= to_date)
                .order_by(News.published_date.desc())
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting stock news for {symbol}: {e}")
            raise

    def get_gradings(self, symbol: str, limit: int = 50) -> list[CompanyGrading]:
        """Retrieve gradings for a company."""
        try:
            return (
                self._db.query(CompanyGrading)
                .filter(CompanyGrading.symbol == symbol)
                .order_by(CompanyGrading.date.desc())
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting gradings for {symbol}: {e}")
            raise

    def get_grading_summary(self, symbol: str) -> CompanyGrading | None:
        """Retrieve the grading summary for a company."""
        try:
            return (
                self._db.query(CompanyGradingSummary)
                .filter(CompanyGradingSummary.symbol == symbol)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting grading summary for {symbol}: {e}")
            raise
