import datetime

from pydantic import BaseModel, ConfigDict


class FinancialHealth(BaseModel):
    company_id: int
    symbol: str
    section: str
    metric: str
    benchmark: str
    value: str
    status: str
    insight: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FinancialHealthWrite(FinancialHealth):
    model_config = ConfigDict(from_attributes=True)


class FinancialHealthRead(FinancialHealth):
    id: int
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    model_config = ConfigDict(from_attributes=True)
