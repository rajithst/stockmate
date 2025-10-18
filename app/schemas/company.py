from typing import List, Optional

from pydantic import BaseModel, ConfigDict, HttpUrl

from app.schemas.grading import CompanyGradingRead
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)


class Company(BaseModel):
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


class CompanyRead(Company):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CompanyWrite(Company):
    model_config = ConfigDict(from_attributes=True)


class CompanyPageResponse(BaseModel):
    company: CompanyRead
    grading_summary: Optional[CompanyGradingRead]
    price_target_news: List[CompanyPriceTargetNewsRead] = []
    general_news: List[CompanyGeneralNewsRead] = []
    grading_news: List[CompanyGradingNewsRead] = []

    model_config = ConfigDict(from_attributes=True)
