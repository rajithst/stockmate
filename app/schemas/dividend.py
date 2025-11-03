from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyDividend(BaseModel):
    symbol: str
    date: date_type
    record_date: Optional[date_type | None] = None
    payment_date: Optional[date_type | None] = None
    declaration_date: Optional[date_type | None] = None
    dividend: Optional[float] = None
    adj_dividend: Optional[float] = None
    dividend_yield: Optional[float] = None
    frequency: Optional[str] = None


class CompanyDividendWrite(CompanyDividend):
    model_config = ConfigDict(from_attributes=True)


class CompanyDividendRead(CompanyDividend):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
