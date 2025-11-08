"""
Consolidated financial health schemas:
- CompanyFinancialHealth: Health indicators and metrics
- CompanyFinancialScore: Financial scoring models (Altman, Piotroski)
"""

import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ========================
# FINANCIAL HEALTH SCHEMAS
# ========================


class CompanyFinancialHealth(BaseModel):
    symbol: str
    section: str
    metric: str
    benchmark: str
    value: str
    status: str
    insight: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialHealthWrite(CompanyFinancialHealth):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialHealthRead(CompanyFinancialHealth):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# FINANCIAL SCORE SCHEMAS
# ========================


class CompanyFinancialScore(BaseModel):
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
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialScoresRead(CompanyFinancialScore):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)
