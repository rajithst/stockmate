from pydantic import BaseModel, ConfigDict, Field
from datetime import date as date_type
from typing import Dict, Any


class FMPRevenueProductSegmentation(BaseModel):
    symbol: str
    fiscal_year: int = Field(..., alias="fiscalYear")
    period: str
    reported_currency: str | None = Field(None, alias="reportedCurrency")
    date: date_type
    segments_data: Dict[str, Any] = Field(..., alias="data")

    model_config = ConfigDict(populate_by_name=True)
