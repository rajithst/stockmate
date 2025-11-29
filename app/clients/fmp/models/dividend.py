from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import date as date_type


class FMPDividend(BaseModel):
    symbol: str
    date: date_type
    record_date: date_type = Field(..., alias="recordDate")
    payment_date: date_type = Field(..., alias="paymentDate")
    declaration_date: date_type = Field(..., alias="declarationDate")
    adj_dividend: float = Field(..., alias="adjDividend")
    dividend: float
    dividend_yield: float = Field(..., alias="yield")
    frequency: str
    currency: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class FMPDividendCalendar(BaseModel):
    symbol: str
    date: date_type
    record_date: date_type = Field(..., alias="recordDate")
    payment_date: date_type = Field(..., alias="paymentDate")
    declaration_date: date_type = Field(..., alias="declarationDate")
    adj_dividend: float = Field(..., alias="adjDividend")
    dividend: float
    dividend_yield: float = Field(..., alias="yield")
    frequency: str

    model_config = ConfigDict(populate_by_name=True)
