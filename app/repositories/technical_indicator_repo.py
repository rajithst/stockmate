import logging
from sqlalchemy.orm import Session

from app.db.models.technical_indicators import CompanyTechnicalIndicator
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class TechnicalIndicatorRepository(BaseRepository):
    """Repository for accessing technical indicator data."""

    def __init__(self, db: Session):
        super().__init__(db)

    def get_technical_indicators_by_symbol(
        self, symbol: str
    ) -> list[CompanyTechnicalIndicator]:
        """Retrieve technical indicators for a given company symbol."""
        return self._get_by_filter(
            CompanyTechnicalIndicator,
            {"symbol": symbol},
            order_by_desc=CompanyTechnicalIndicator.date,
        )
