from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DiscountedCashFlow(BaseModel):
    symbol: str
    date: Optional[str]
    dcf: Optional[float]
    stock_price: Optional[float]


class DiscountedCashFlowRead(DiscountedCashFlow):
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiscountedCashFlowWrite(DiscountedCashFlow):
    model_config = ConfigDict(from_attributes=True)
