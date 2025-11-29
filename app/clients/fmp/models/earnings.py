from datetime import date as date_type
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class FMPEarningsCalendar(BaseModel):
    symbol: str
    date: date_type
    eps_actual: Optional[float] = Field(..., alias="epsActual")
    eps_estimated: Optional[float] = Field(..., alias="epsEstimated")
    revenue_actual: Optional[float] = Field(..., alias="revenueActual")
    revenue_estimated: Optional[float] = Field(..., alias="revenueEstimated")
    last_update: date_type = Field(..., alias="lastUpdated")

    @field_validator("date", mode="before")
    @classmethod
    def convert_date_string_to_date(cls, v):
        """Convert date string (YYYY-MM-DD) to Python date object."""
        if isinstance(v, date_type):
            return v
        if isinstance(v, str):
            return date_type.fromisoformat(v)
        return v

    @field_validator("last_update", mode="before")
    @classmethod
    def convert_last_update_string_to_date(cls, v):
        """Convert last_update date string (YYYY-MM-DD) to Python date object."""
        if isinstance(v, date_type):
            return v
        if isinstance(v, str):
            return date_type.fromisoformat(v)
        return v
