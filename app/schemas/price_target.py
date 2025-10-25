from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyPriceTarget(BaseModel):
    company_id: int
    symbol: str
    target_high: Optional[float]
    target_low: Optional[float]
    target_consensus: Optional[float]
    target_median: Optional[float]


class CompanyPriceTargetRead(CompanyPriceTarget):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetWrite(CompanyPriceTarget):
    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetSummary(BaseModel):
    company_id: int
    symbol: str
    last_month_count: int
    last_month_average_price_target: float
    last_quarter_count: int
    last_quarter_average_price_target: float
    last_year_count: int
    last_year_average_price_target: float
    all_time_count: int
    all_time_average_price_target: float
    publishers: Optional[str]


class CompanyPriceTargetSummaryRead(CompanyPriceTargetSummary):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetSummaryWrite(CompanyPriceTargetSummary):
    model_config = ConfigDict(from_attributes=True)
