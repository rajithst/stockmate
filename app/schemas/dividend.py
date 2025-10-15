from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyDividend(BaseModel):
    company_id: int
    symbol: str
    date: str
    record_date: Optional[str] = None
    payment_date: Optional[str] = None
    declaration_date: Optional[str] = None
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
