from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class StockPriceChangeBase(BaseModel):
    company_id: int
    symbol: str
    one_day: Optional[float] = None
    five_day: Optional[float] = None
    one_month: Optional[float] = None
    three_month: Optional[float] = None
    six_month: Optional[float] = None
    ytd: Optional[float] = None
    one_year: Optional[float] = None
    three_year: Optional[float] = None
    five_year: Optional[float] = None
    ten_year: Optional[float] = None


class StockPriceChangeWrite(StockPriceChangeBase):
    model_config = ConfigDict(from_attributes=True)


class StockPriceChangeRead(StockPriceChangeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
