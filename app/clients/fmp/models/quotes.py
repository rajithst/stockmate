from pydantic import BaseModel, ConfigDict, Field


class FMPStockPriceChange(BaseModel):
    symbol: str
    one_day: float = Field(..., alias="1D")
    five_day: float = Field(..., alias="5D")
    one_month: float = Field(..., alias="1M")
    three_month: float = Field(..., alias="3M")
    six_month: float = Field(..., alias="6M")
    ytd: float = Field(..., alias="ytd")
    one_year: float = Field(..., alias="1Y")
    three_year: float = Field(..., alias="3Y")
    five_year: float = Field(..., alias="5Y")
    ten_year: float = Field(..., alias="10Y")

    model_config = ConfigDict(populate_by_name=True)
