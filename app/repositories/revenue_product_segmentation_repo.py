"""Revenue product segmentation repository for managing segmentation data access."""

import logging

from sqlalchemy.orm import Session

from app.db.models.company_metrics import CompanyRevenueProductSegmentation
from app.repositories.base_repo import BaseRepository
from app.schemas.company_metrics import CompanyRevenueProductSegmentationWrite

logger = logging.getLogger(__name__)


class CompanyRevenueProductSegmentationRepository(
    BaseRepository[CompanyRevenueProductSegmentation]
):
    """Repository for CompanyRevenueProductSegmentation operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def upsert_revenue_segmentations(
        self,
        segmentations_in: list[CompanyRevenueProductSegmentationWrite],
    ) -> list[CompanyRevenueProductSegmentation]:
        """Upsert revenue product segmentation records."""
        return self._upsert_records(
            segmentations_in,
            CompanyRevenueProductSegmentation,
            lambda seg: {
                "symbol": seg.symbol,
                "date": seg.date,
                "period": seg.period,
            },
            "upsert_revenue_product_segmentation",
        )
