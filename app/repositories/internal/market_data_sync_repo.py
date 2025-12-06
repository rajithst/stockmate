import logging
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.grading import CompanyGrading, CompanyGradingSummary
from app.db.models.news import (
    News,
)
from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary
from app.db.models.ratings import CompanyRatingSummary
from app.schemas.market_data import (
    CompanyGradingWrite,
    CompanyGradingSummaryWrite,
    CompanyPriceTargetWrite,
    CompanyPriceTargetSummaryWrite,
    CompanyRatingSummaryWrite,
    NewsWrite,
)
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class CompanyMarketDataSyncRepository:
    """Repository for market data entities (grading, rating, price target, news)."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def upsert_grading(
        self, symbol: str, grading_data: list[CompanyGradingWrite]
    ) -> list[CompanyGrading]:
        """Bulk upsert gradings by symbol and date."""
        try:
            results = []
            for grading_in in grading_data:
                # Find existing record
                existing = (
                    self._db.query(CompanyGrading)
                    .filter_by(symbol=symbol, date=grading_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, grading_in)
                else:
                    # Create new
                    result = CompanyGrading(**grading_in.model_dump(exclude_unset=True))
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} gradings for symbol {symbol}")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_grading: {e}")
            raise

    def upsert_grading_summary(
        self, summary_data: CompanyGradingSummaryWrite
    ) -> CompanyGradingSummary:
        """Upsert grading summary by symbol."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyGradingSummary)
                .filter_by(symbol=summary_data.symbol)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, summary_data)
            else:
                # Create new
                result = CompanyGradingSummary(
                    **summary_data.model_dump(exclude_unset=True)
                )
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(f"Upserted grading summary for symbol {summary_data.symbol}")
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_grading_summary: {e}")
            raise

    def upsert_rating_summary(
        self, rating: CompanyRatingSummaryWrite
    ) -> CompanyRatingSummary:
        """Upsert rating summary by symbol."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyRatingSummary)
                .filter_by(symbol=rating.symbol)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, rating)
            else:
                # Create new
                result = CompanyRatingSummary(**rating.model_dump(exclude_unset=True))
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(f"Upserted rating summary for symbol {rating.symbol}")
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_rating_summary: {e}")
            raise

    def upsert_price_target(
        self, price_targets: CompanyPriceTargetWrite
    ) -> CompanyPriceTarget:
        """Upsert price target by symbol."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyPriceTarget)
                .filter_by(symbol=price_targets.symbol)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, price_targets)
            else:
                # Create new
                result = CompanyPriceTarget(
                    **price_targets.model_dump(exclude_unset=True)
                )
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(f"Upserted price target for symbol {price_targets.symbol}")
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_price_target: {e}")
            raise

    def upsert_price_target_summary(
        self, summary_data: CompanyPriceTargetSummaryWrite
    ) -> CompanyPriceTargetSummary:
        """Upsert price target summary by symbol."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyPriceTargetSummary)
                .filter_by(symbol=summary_data.symbol)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, summary_data)
            else:
                # Create new
                result = CompanyPriceTargetSummary(
                    **summary_data.model_dump(exclude_unset=True)
                )
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(
                f"Upserted price target summary for symbol {summary_data.symbol}"
            )
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_price_target_summary: {e}")
            raise

    def upsert_stock_news(self, news_data: List[NewsWrite]) -> List[News]:
        """Bulk upsert stock news articles by symbol and title."""
        try:
            results = []
            for news_in in news_data:
                # Find existing record
                existing = (
                    self._db.query(News)
                    .filter_by(symbol=news_in.symbol, title=news_in.title)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, news_in)
                else:
                    # Create new
                    result = News(**news_in.model_dump(exclude_unset=True))
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} stock news articles")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_stock_news: {e}")
            raise

    def upsert_general_news(self, news_data: List[NewsWrite]) -> List[News]:
        """Bulk upsert general news articles by publisher, title, and published_date."""
        try:
            results = []
            for news_in in news_data:
                # Find existing record
                existing = (
                    self._db.query(News)
                    .filter_by(
                        publisher=news_in.publisher,
                        title=news_in.title,
                        published_date=news_in.published_date,
                    )
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, news_in)
                else:
                    # Create new
                    result = News(**news_in.model_dump(exclude_unset=True))
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} general news articles")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_general_news: {e}")
            raise
