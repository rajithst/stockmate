from pytest import Session
from app.db.models.technical_indicators import CompanyTechnicalIndicator


class TechnicalIndicatorRepository:
    """Repository for accessing technical indicator data."""

    def __init__(self, db: Session):
        self._db = db

    def get_technical_indicators_by_symbol(
        self, symbol: str
    ) -> list[CompanyTechnicalIndicator]:
        """Retrieve technical indicators for a given company symbol."""
        return (
            self._db.query(CompanyTechnicalIndicator)
            .filter(CompanyTechnicalIndicator.symbol == symbol)
            .all()
        )
