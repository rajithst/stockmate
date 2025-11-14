import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.financial_health import CompanyFinancialHealth


logger = logging.getLogger(__name__)


class CompanyFinancialHealthRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_financial_health(self, symbol: str) -> list[CompanyFinancialHealth]:
        """Retrieve financial health data for a company."""
        try:
            return (
                self._db.query(CompanyFinancialHealth)
                .filter(CompanyFinancialHealth.symbol == symbol)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting financial health for {symbol}: {e}")
            raise

    def get_financial_scores(self, symbol: str) -> CompanyFinancialHealth | None:
        """Retrieve financial scores for a company."""
        try:
            return (
                self._db.query(CompanyFinancialHealth)
                .filter(CompanyFinancialHealth.symbol == symbol)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting financial scores for {symbol}: {e}")
            raise
