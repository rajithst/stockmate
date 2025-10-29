import datetime

from pydantic import BaseModel, ConfigDict


class CompanyFinancialHealth(BaseModel):
    company_id: int
    symbol: str
    section: str
    metric: str
    benchmark: str
    value: str
    status: str
    insight: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialHealthWrite(CompanyFinancialHealth):
    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialHealthRead(CompanyFinancialHealth):
    id: int
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    model_config = ConfigDict(from_attributes=True)
