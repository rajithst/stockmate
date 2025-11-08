import logging

from sqlalchemy.orm import Session

from app.db.models.company_metrics import CompanyAnalystEstimate
from app.repositories.base_repo import BaseRepository
from app.schemas.company_metrics import CompanyAnalystEstimateWrite

logger = logging.getLogger(__name__)


class CompanyAnalystEstimateRepository(BaseRepository[CompanyAnalystEstimate]):
    """Repository for CompanyAnalystEstimate operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def upsert_analyst_estimates(
        self, estimates: list[CompanyAnalystEstimateWrite]
    ) -> list[CompanyAnalystEstimate]:
        """Bulk upsert analyst estimates."""
        return self._upsert_records(
            estimates,
            CompanyAnalystEstimate,
            lambda est: {
                "company_id": est.company_id,
                "date": est.date,
            },
            "upsert_analyst_estimates",
        )
