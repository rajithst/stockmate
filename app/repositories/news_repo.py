from typing import List

from sqlalchemy.orm import Session

from app.db.models.news import (
    CompanyGeneralNews,
    CompanyGradingNews,
    CompanyPriceTargetNews,
)
from app.schemas.news import (
    CompanyGeneralNewsWrite,
    CompanyGradingNewsWrite,
    CompanyPriceTargetNewsWrite,
)


class CompanyNewsRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_general_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[CompanyGeneralNews]:
        """Retrieve general news articles for a given company symbol."""
        return (
            self._db.query(CompanyGeneralNews)
            .filter(CompanyGeneralNews.symbol == symbol)
            .order_by(CompanyGeneralNews.published_date.desc())
            .limit(limit)
            .all()
        )

    def get_price_target_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[CompanyPriceTargetNews]:
        """Retrieve price target news articles for a given company symbol."""
        return (
            self._db.query(CompanyPriceTargetNews)
            .filter(CompanyPriceTargetNews.symbol == symbol)
            .order_by(CompanyPriceTargetNews.published_date.desc())
            .limit(limit)
            .all()
        )

    def get_grading_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[CompanyGradingNews]:
        """Retrieve stock grading news articles for a given company symbol."""
        return (
            self._db.query(CompanyGradingNews)
            .filter(CompanyGradingNews.symbol == symbol)
            .order_by(CompanyGradingNews.published_date.desc())
            .limit(limit)
            .all()
        )

    def upsert_general_news(
        self, news_data: List[CompanyGeneralNewsWrite]
    ) -> List[CompanyGeneralNews]:
        """Insert or update general news articles."""
        news_records = []
        for news in news_data:
            existing = (
                self._db.query(CompanyGeneralNews)
                .filter_by(symbol=news.symbol, title=news.title)
                .first()
            )
            if existing:
                for key, value in news.model_dump(exclude_unset=True).items():
                    setattr(existing, key, value)
                news_record = existing
            else:
                news_record = CompanyGeneralNews(**news.model_dump(exclude_unset=True))
                self._db.add(news_record)
            news_records.append(news_record)
        self._db.commit()
        for record in news_records:
            self._db.refresh(record)
        return news_records

    def upsert_price_target_news(
        self, news_data: List[CompanyPriceTargetNewsWrite]
    ) -> List[CompanyPriceTargetNews]:
        """Insert or update price target news articles."""
        news_records = []
        for news in news_data:
            existing = (
                self._db.query(CompanyPriceTargetNews)
                .filter_by(symbol=news.symbol, title=news.title)
                .first()
            )
            if existing:
                for key, value in news.model_dump(exclude_unset=True).items():
                    setattr(existing, key, value)
                news_record = existing
            else:
                news_record = CompanyPriceTargetNews(
                    **news.model_dump(exclude_unset=True)
                )
                self._db.add(news_record)
            news_records.append(news_record)
        self._db.commit()
        for record in news_records:
            self._db.refresh(record)
        return news_records

    def upsert_grading_news(
        self, news_data: List[CompanyGradingNewsWrite]
    ) -> List[CompanyGradingNews]:
        """Insert or update stock grading news articles."""
        news_records = []
        for news in news_data:
            existing = (
                self._db.query(CompanyGradingNews)
                .filter_by(symbol=news.symbol, title=news.title)
                .first()
            )
            if existing:
                for key, value in news.model_dump(exclude_unset=True).items():
                    setattr(existing, key, value)
                news_record = existing
            else:
                news_record = CompanyGradingNews(**news.model_dump(exclude_unset=True))
                self._db.add(news_record)
            news_records.append(news_record)
        self._db.commit()
        for record in news_records:
            self._db.refresh(record)
        return news_records
