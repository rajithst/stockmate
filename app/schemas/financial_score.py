from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyFinancialScore(BaseModel):
    company_id: int
    symbol: str
    reported_currency: Optional[str] = None
    altman_z_score: Optional[float] = None
    piotroski_score: Optional[int] = None
    working_capital: Optional[float] = None
    total_assets: Optional[float] = None
    retained_earnings: Optional[float] = None
    ebit: Optional[float] = None
    market_cap: Optional[float] = None
    total_liabilities: Optional[float] = None
    revenue: Optional[float] = None


class CompanyFinancialScoresWrite(CompanyFinancialScore):
    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialScoresRead(CompanyFinancialScore):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
