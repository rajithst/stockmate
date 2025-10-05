from pydantic import BaseModel, Field

class Earnings(BaseModel):
    symbol: str
    date: str
    eps_actual: float = Field(..., alias="epsActual")
    eps_estimated: float = Field(..., alias="epsEstimated")
    revenue_actual: int = Field(..., alias="revenueActual")
    revenue_estimated: int = Field(..., alias="revenueEstimated")
    last_updated: str = Field(..., alias="lastUpdated")

    class Config:
        populate_by_name = True
