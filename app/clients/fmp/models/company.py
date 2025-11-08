from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class FMPCompanyProfile(BaseModel):
    symbol: str
    company_name: str = Field(..., alias="companyName")
    price: float
    market_cap: float = Field(..., alias="marketCap")
    currency: str
    exchange_full_name: str = Field(..., alias="exchangeFullName")
    exchange: str
    industry: str
    website: HttpUrl
    description: str
    sector: str
    country: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    image: Optional[HttpUrl] = None
    ipo_date: Optional[date] = Field(..., alias="ipoDate")
    default_image: Optional[bool] = Field(..., alias="defaultImage")

    model_config = ConfigDict(populate_by_name=True)
