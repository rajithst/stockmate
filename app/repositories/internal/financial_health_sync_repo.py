import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.financial_health import CompanyFinancialHealth
from app.db.models.financial_score import CompanyFinancialScore
from app.schemas.financial_health import (
    CompanyFinancialHealthWrite,
    CompanyFinancialScoresWrite,
)
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class CompanyFinancialHealthSyncRepository:
    """Repository for financial health and financial scores entities."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def upsert_financial_scores(
        self, financial_scores: CompanyFinancialScoresWrite
    ) -> CompanyFinancialScore | None:
        """Upsert financial scores by symbol."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyFinancialScore)
                .filter_by(symbol=financial_scores.symbol)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, financial_scores)
            else:
                # Create new
                result = CompanyFinancialScore(
                    **financial_scores.model_dump(exclude_unset=True)
                )
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(
                f"Upserted financial scores for symbol {financial_scores.symbol}"
            )
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_financial_scores: {e}")
            raise

    def upsert_financial_health(
        self, financial_health: list[CompanyFinancialHealthWrite]
    ) -> list[CompanyFinancialHealth]:
        """Bulk upsert financial health data by symbol, section, and metric."""
        try:
            results = []
            for health_in in financial_health:
                # Find existing record
                existing = (
                    self._db.query(CompanyFinancialHealth)
                    .filter_by(
                        symbol=health_in.symbol,
                        section=health_in.section,
                        metric=health_in.metric,
                    )
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, health_in)
                else:
                    # Create new
                    result = CompanyFinancialHealth(
                        **health_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} financial health records")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_financial_health: {e}")
            raise
