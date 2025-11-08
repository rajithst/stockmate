from typing import List
import logging

from sqlalchemy.orm import Session

from app.db.models.news import (
    CompanyGeneralNews,
    CompanyGradingNews,
    CompanyPriceTargetNews,
    CompanyStockNews,
)
from app.schemas.market_data import (
    CompanyGeneralNewsWrite,
    CompanyGradingNewsWrite,
    CompanyPriceTargetNewsWrite,
    CompanyStockNewsWrite,
)
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class CompanyNewsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_general_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[CompanyGeneralNews]:
        """Retrieve general news articles for a given company symbol."""
        return self._get_by_filter(
            CompanyGeneralNews,
            {"symbol": symbol},
            order_by_desc=CompanyGeneralNews.published_date,
            limit=limit,
        )

    def get_price_target_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[CompanyPriceTargetNews]:
        """Retrieve price target news articles for a given company symbol."""
        return self._get_by_filter(
            CompanyPriceTargetNews,
            {"symbol": symbol},
            order_by_desc=CompanyPriceTargetNews.published_date,
            limit=limit,
        )

    def get_grading_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[CompanyGradingNews]:
        """Retrieve stock grading news articles for a given company symbol."""
        return self._get_by_filter(
            CompanyGradingNews,
            {"symbol": symbol},
            order_by_desc=CompanyGradingNews.published_date,
            limit=limit,
        )

    def upsert_general_news(
        self, news_data: List[CompanyGeneralNewsWrite]
    ) -> List[CompanyGeneralNews]:
        """Insert or update general news articles."""
        return self._upsert_records(
            news_data,
            CompanyGeneralNews,
            lambda news: {
                "publisher": news.publisher,
                "title": news.title,
                "published_date": news.published_date,
            },
            "upsert_general_news",
        )

    def upsert_price_target_news(
        self, news_data: List[CompanyPriceTargetNewsWrite]
    ) -> List[CompanyPriceTargetNews]:
        """Insert or update price target news articles."""
        return self._upsert_records(
            news_data,
            CompanyPriceTargetNews,
            lambda news: {"symbol": news.symbol, "title": news.title},
            "upsert_price_target_news",
        )

    def upsert_grading_news(
        self, news_data: List[CompanyGradingNewsWrite]
    ) -> List[CompanyGradingNews]:
        """Insert or update stock grading news articles."""
        return self._upsert_records(
            news_data,
            CompanyGradingNews,
            lambda news: {"symbol": news.symbol, "title": news.title},
            "upsert_grading_news",
        )

    def upsert_stock_news(
        self, news_data: List[CompanyStockNewsWrite]
    ) -> List[CompanyStockNews]:
        """Insert or update stock news articles."""
        return self._upsert_records(
            news_data,
            CompanyStockNews,
            lambda news: {"symbol": news.symbol, "title": news.title},
            "upsert_stock_news",
        )
