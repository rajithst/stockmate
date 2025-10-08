from pydantic import BaseModel, HttpUrl, ConfigDict


class CompanyIn(BaseModel):
    symbol: str
    company_name: str
    price: float
    market_cap: int
    currency: str
    exchange_full_name: str
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
    ipo_date: str

class CompanyRead(CompanyIn):
    id: int

    model_config = ConfigDict(from_attributes=True)
