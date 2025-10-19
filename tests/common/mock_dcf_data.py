from app.schemas.dcf import DiscountedCashFlowRead
from app.db.models.dcf import DiscountedCashFlow


class MockDiscountedCashFlowDataBuilder:
    @staticmethod
    def discounted_cash_flow_read(**overrides) -> DiscountedCashFlowRead:
        data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "date": "2023-10-01",
            "dcf": 175.0,
            "stock_price": 160.0,
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        data.update(overrides)
        return DiscountedCashFlowRead.model_validate(data)

    @staticmethod
    def save_discounted_cash_flow(db_session, **overrides) -> DiscountedCashFlow:
        data = {
            "company_id": 1,
            "symbol": "TEST",
            "date": "2023-10-01",
            "dcf": 175.0,
            "stock_price": 160.0,
        }
        dcf_data = {**data, **overrides}
        dcf = DiscountedCashFlow(**dcf_data)
        db_session.add(dcf)
        db_session.commit()
        db_session.refresh(dcf)
        return dcf
