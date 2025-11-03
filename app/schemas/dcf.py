from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DiscountedCashFlow(BaseModel):
    company_id: int
    symbol: str
    date: date_type
    dcf: float
    stock_price: Optional[float]


class DiscountedCashFlowRead(DiscountedCashFlow):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DiscountedCashFlowWrite(DiscountedCashFlow):
    model_config = ConfigDict(from_attributes=True)
