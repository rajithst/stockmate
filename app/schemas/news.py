from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyGeneralNews(BaseModel):
    company_id: Optional[int]
    symbol: Optional[str]
    published_date: datetime
    publisher: str
    news_title: str
    news_url: str
    text: str
    image: Optional[str]
    site: Optional[str]


class CompanyGeneralNewsRead(CompanyGeneralNews):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class CompanyGeneralNewsWrite(CompanyGeneralNews):
    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetNews(BaseModel):
    company_id: int
    symbol: str
    published_date: datetime
    news_url: str
    news_title: str
    analyst_name: str
    price_target: float
    adj_price_target: Optional[float] = None
    price_when_posted: float
    news_publisher: Optional[str] = None
    news_base_url: Optional[str] = None
    analyst_company: Optional[str] = None


class CompanyPriceTargetNewsWrite(CompanyPriceTargetNews):
    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetNewsRead(CompanyPriceTargetNews):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyGradingNews(BaseModel):
    company_id: int
    symbol: str
    published_date: datetime
    news_url: str
    news_title: str
    news_base_url: Optional[str] = None
    news_publisher: Optional[str] = None
    new_grade: str
    previous_grade: Optional[str] = None
    grading_company: Optional[str] = None
    action: Optional[str] = None
    price_when_posted: float


class CompanyGradingNewsWrite(CompanyGradingNews):
    model_config = ConfigDict(from_attributes=True)


class CompanyGradingNewsRead(CompanyGradingNews):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
