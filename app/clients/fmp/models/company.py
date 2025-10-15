from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class FMPCompanyProfile(BaseModel):
    symbol: str
    company_name: str = Field(..., alias="companyName")
    price: float
    market_cap: int = Field(..., alias="marketCap")
    currency: str
    exchange_full_name: str = Field(..., alias="exchangeFullName")
    exchange: str
    industry: str
    website: HttpUrl
    description: str
    sector: str
    country: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    image: HttpUrl
    ipo_date: str = Field(..., alias="ipoDate")
    default_image: bool = Field(..., alias="defaultImage")

    model_config = ConfigDict(populate_by_name=True)
