from pydantic import BaseModel, ConfigDict, Field


class FMPDividend(BaseModel):
    symbol: str
    date: str
    record_date: str = Field(..., alias="recordDate")
    payment_date: str = Field(..., alias="paymentDate")
    declaration_date: str = Field(..., alias="declarationDate")
    adj_dividend: float = Field(..., alias="adjDividend")
    dividend: float
    dividend_yield: float = Field(..., alias="yield")
    frequency: str

    model_config = ConfigDict(populate_by_name=True)
