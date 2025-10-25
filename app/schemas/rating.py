from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyRatingSummary(BaseModel):
    company_id: int
    symbol: str
    rating: Optional[str]
    overall_score: Optional[int]
    discounted_cash_flow_score: Optional[int]
    return_on_equity_score: Optional[int]
    return_on_assets_score: Optional[int]
    debt_to_equity_score: Optional[int]
    price_to_earnings_score: Optional[int]
    price_to_book_score: Optional[int]


class CompanyRatingSummaryRead(CompanyRatingSummary):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyRatingSummaryWrite(CompanyRatingSummary):
    model_config = ConfigDict(from_attributes=True)
