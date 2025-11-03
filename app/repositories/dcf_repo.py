import logging
from sqlalchemy.orm import Session

from app.db.models.dcf import DiscountedCashFlow
from app.schemas.dcf import DiscountedCashFlowWrite
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class DiscountedCashFlowRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def upsert_discounted_cash_flow(
        self, dcf_in: DiscountedCashFlowWrite
    ) -> DiscountedCashFlow:
        """Upsert DCF record by company_id."""
        return self._upsert_single(
            dcf_in,
            DiscountedCashFlow,
            lambda dcf: {"company_id": dcf.company_id},
            "upsert_discounted_cash_flow",
        )
