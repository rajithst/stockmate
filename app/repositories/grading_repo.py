import logging

from sqlalchemy.orm import Session

from app.db.models.grading import CompanyGrading, CompanyGradingSummary
from app.repositories.base_repo import BaseRepository
from app.schemas.grading import CompanyGradingSummaryWrite, CompanyGradingWrite

logger = logging.getLogger(__name__)


class GradingRepository(BaseRepository):
    """Repository for managing CompanyGrading records."""

    def __init__(self, session: Session):
        super().__init__(session)

    def get_gradings_by_symbol(
        self, symbol: str, limit: int = 100
    ) -> list[CompanyGrading]:
        return self._get_by_filter(
            CompanyGrading,
            {"symbol": symbol},
            order_by_desc=CompanyGrading.date,
            limit=limit,
        )

    def upsert_grading(
        self, symbol: str, grading_data: list[CompanyGradingWrite]
    ) -> list[CompanyGrading]:
        """Upsert gradings using the base class pattern."""
        return self._upsert_records(
            grading_data,
            CompanyGrading,
            lambda g: {"symbol": symbol, "date": g.date},
            "upsert_grading",
        )


class GradingSummaryRepository(BaseRepository):
    """Repository for managing CompanyGradingSummary records."""

    def __init__(self, session: Session):
        super().__init__(session)

    def upsert_grading_summary(
        self, summary_data: CompanyGradingSummaryWrite
    ) -> CompanyGradingSummary:
        """Upsert grading summary by symbol."""
        return self._upsert_single(
            summary_data,
            CompanyGradingSummary,
            lambda s: {"symbol": s.symbol},
            "upsert_grading_summary",
        )
