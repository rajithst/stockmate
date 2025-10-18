from pydantic import BaseModel, ConfigDict, Field


class FMPEarnings(BaseModel):
    symbol: str
    date: str
    eps_actual: float = Field(..., alias="epsActual")
    eps_estimated: float = Field(..., alias="epsEstimated")
    revenue_actual: int = Field(..., alias="revenueActual")
    revenue_estimated: int = Field(..., alias="revenueEstimated")
    last_updated: str = Field(..., alias="lastUpdated")

    model_config = ConfigDict(populate_by_name=True)
