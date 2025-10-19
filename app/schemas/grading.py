from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyGrading(BaseModel):
    company_id: int
    symbol: str
    date: str
    grading_company: Optional[str] = None
    previous_grade: Optional[str] = None
    new_grade: Optional[str] = None
    action: Optional[str] = None


class CompanyGradingWrite(CompanyGrading):
    model_config = ConfigDict(from_attributes=True)


class CompanyGradingRead(CompanyGrading):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyGradingSummary(BaseModel):
    company_id: int
    symbol: str
    buy: int
    hold: int
    sell: int
    strong_buy: int
    strong_sell: int
    consensus: str


class CompanyGradingSummaryRead(CompanyGradingSummary):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyGradingSummaryWrite(CompanyGradingSummary):
    model_config = ConfigDict(from_attributes=True)
