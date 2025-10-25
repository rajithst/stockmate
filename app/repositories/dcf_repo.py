from sqlalchemy.orm import Session

from app.db.models.dcf import DiscountedCashFlow
from app.schemas.dcf import DiscountedCashFlowWrite
from app.util.model_mapper import map_model


class DiscountedCashFlowRepository:
    def __init__(self, session: Session):
        self._session = session

    def upsert_discounted_cash_flow(
        self, dcf_in: DiscountedCashFlowWrite
    ) -> DiscountedCashFlow:
        dcf = (
            self._session.query(DiscountedCashFlow)
            .filter(DiscountedCashFlow.company_id == dcf_in.company_id)
            .one_or_none()
        )
        if dcf:
            dcf = map_model(dcf, dcf_in)
        else:
            dcf = DiscountedCashFlow(**dcf_in.model_dump())
            self._session.add(dcf)

        self._session.commit()
        self._session.refresh(dcf)
        return dcf
