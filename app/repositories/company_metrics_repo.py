import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.company_metrics import CompanyAnalystEstimate
from app.db.models.company_metrics import CompanyKeyMetrics

logger = logging.getLogger(__name__)


class CompanyMetricsRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_key_metrics(self, symbol: str, limit: int = 50) -> list[CompanyKeyMetrics]:
        """Retrieve key metrics for a company."""

        try:
            return (
                self._db.query(CompanyKeyMetrics)
                .filter(CompanyKeyMetrics.symbol == symbol)
                .order_by(
                    CompanyKeyMetrics.date.desc(), CompanyKeyMetrics.fiscal_year.desc()
                )
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting key metrics for {symbol}: {e}")
            raise

    def get_analyst_estimates(self, symbol: str, limit: int = 50) -> list[CompanyAnalystEstimate]:
        """Retrieve analyst estimates for a company."""
        try:
            return (
                self._db.query(CompanyAnalystEstimate)
                .filter(CompanyKeyMetrics.symbol == symbol)
                .order_by(CompanyKeyMetrics.date.desc())
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting analyst estimates for {symbol}: {e}")
            raise
