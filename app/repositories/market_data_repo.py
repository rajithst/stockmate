import enum
import logging
from typing import TypeVar

from sqlalchemy.orm import Session

from app.db.models.grading import CompanyGrading, CompanyGradingSummary
from app.db.models.news import (
    CompanyGeneralNews,
    CompanyGradingNews,
    CompanyPriceTargetNews,
    CompanyStockNews,
)
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)


class CompanyNewsType(enum.Enum):
    GENERAL = "general"
    PRICE_TARGET = "price_target"
    GRADING = "grading"
    STOCK = "stock"


NewsType = TypeVar(
    "NewsType",
    CompanyGeneralNews,
    CompanyPriceTargetNews,
    CompanyGradingNews,
    CompanyStockNews,
)


class CompanyMarketDataRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_company_news(
        self, symbol: str, news_type: CompanyNewsType, limit: int = 50
    ) -> list[NewsType]:
        """Retrieve news articles for a company based on the news type."""
        if news_type == CompanyNewsType.GENERAL:
            target_model = CompanyGeneralNews
        elif news_type == CompanyNewsType.PRICE_TARGET:
            target_model = CompanyPriceTargetNews
        elif news_type == CompanyNewsType.GRADING:
            target_model = CompanyGradingNews
        elif news_type == CompanyNewsType.STOCK:
            target_model = CompanyStockNews
        else:
            logger.error(f"Unsupported news type: {news_type}")
            return []

        try:
            return (
                self._db.query(target_model)
                .filter(target_model.symbol == symbol)
                .order_by(target_model.published_date.desc())
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting {news_type.value} news for {symbol}: {e}")
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
