from typing import List, Type, Any

from sqlalchemy.orm import Session

from app.db.models import CompanyGeneralNews, CompanyGradingNews
from app.schemas.news import CompanyGeneralNewsWrite


class CompanyNewsRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_general_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[type[CompanyGeneralNews]]:
        """Retrieve general news articles for a given company symbol."""
        return (
            self._db.query(CompanyGeneralNews)
            .filter(CompanyGeneralNews.symbol == symbol)
            .order_by(CompanyGeneralNews.published_date.desc())
            .limit(limit)
            .all()
        )

    def create_general_news(
        self, news_data: List[CompanyGeneralNewsWrite]
    ) -> list[CompanyGeneralNews]:
        """Create multiple general news records."""
        news_records = [CompanyGeneralNews(**data.model_dump()) for data in news_data]
        self._db.bulk_save_objects(news_records)
        self._db.commit()
        return news_records

    def delete_general_news_by_symbol(
        self, symbol: str, from_date: str, to_date: str
    ) -> int:
        """Delete general news articles for a given company symbol within a date range."""
        deleted = (
            self._db.query(CompanyGeneralNews)
            .filter(
                CompanyGeneralNews.symbol == symbol,
                CompanyGeneralNews.published_date >= from_date,
                CompanyGeneralNews.published_date <= to_date,
            )
            .delete(synchronize_session=False)
        )
        self._db.commit()
        return deleted

    def get_price_target_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[type[CompanyGeneralNews]]:
        """Retrieve price target news articles for a given company symbol."""
        return (
            self._db.query(CompanyGeneralNews)
            .filter(CompanyGeneralNews.symbol == symbol)
            .order_by(CompanyGeneralNews.published_date.desc())
            .limit(limit)
            .all()
        )

    def create_price_target_news(
        self, news_data: List[CompanyGeneralNewsWrite]
    ) -> list[CompanyGeneralNews]:
        """Create multiple price target news records."""
        news_records = [CompanyGeneralNews(**data.model_dump()) for data in news_data]
        self._db.bulk_save_objects(news_records)
        self._db.commit()
        return news_records

    def delete_price_target_news_by_symbol(
        self, symbol: str, from_date: str, to_date: str
    ) -> int:
        """Delete price target news articles for a given company symbol within a date range."""
        deleted = (
            self._db.query(CompanyGeneralNews)
            .filter(
                CompanyGeneralNews.symbol == symbol,
                CompanyGeneralNews.published_date >= from_date,
                CompanyGeneralNews.published_date <= to_date,
            )
            .delete(synchronize_session=False)
        )
        self._db.commit()
        return deleted

    def get_grading_news_by_symbol(
        self, symbol: str, limit: int = 20
    ) -> list[type[CompanyGeneralNews]]:
        """Retrieve stock grading news articles for a given company symbol."""
        return (
            self._db.query(CompanyGeneralNews)
            .filter(CompanyGeneralNews.symbol == symbol)
            .order_by(CompanyGeneralNews.published_date.desc())
            .limit(limit)
            .all()
        )

    def create_stock_grading_news(
        self, news_data: List[CompanyGeneralNewsWrite]
    ) -> list[CompanyGeneralNews]:
        """Create multiple stock grading news records."""
        news_records = [CompanyGeneralNews(**data.model_dump()) for data in news_data]
        self._db.bulk_save_objects(news_records)
        self._db.commit()
        return news_records

    def delete_stock_grading_news_by_symbol(
        self, symbol: str, from_date: str, to_date: str
    ) -> int:
        """Delete stock grading news articles for a given company symbol within a date range."""
        deleted = (
            self._db.query(CompanyGeneralNews)
            .filter(
                CompanyGeneralNews.symbol == symbol,
                CompanyGeneralNews.published_date >= from_date,
                CompanyGeneralNews.published_date <= to_date,
            )
            .delete(synchronize_session=False)
        )
        self._db.commit()
        return deleted
