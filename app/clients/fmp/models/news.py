from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class FMPStockNews(BaseModel):
    symbol: str
    published_date: datetime = Field(..., alias="publishedDate")
    publisher: str
    title: str
    image: HttpUrl
    site: str
    text: str
    url: HttpUrl

    model_config = ConfigDict(populate_by_name=True)


class FMPGeneralNews(BaseModel):
    symbol: Optional[str] = None
    published_date: datetime = Field(..., alias="publishedDate")
    publisher: str
    title: str
    image: HttpUrl
    site: str
    text: str
    url: HttpUrl

    model_config = ConfigDict(populate_by_name=True)


class FMPPriceTargetNews(BaseModel):
    symbol: str
    published_date: datetime = Field(..., alias="publishedDate")
    news_url: HttpUrl = Field(..., alias="newsURL")
    news_title: str = Field(..., alias="newsTitle")
    analyst_name: str = Field(..., alias="analystName")
    price_target: float = Field(..., alias="priceTarget")
    adj_price_target: float = Field(..., alias="adjPriceTarget")
    price_when_posted: float = Field(..., alias="priceWhenPosted")
    news_publisher: str = Field(..., alias="newsPublisher")
    news_base_url: str = Field(..., alias="newsBaseURL")
    analyst_company: str = Field(..., alias="analystCompany")

    model_config = ConfigDict(populate_by_name=True)


class FMPStockGradingNews(BaseModel):
    symbol: str
    published_date: datetime = Field(..., alias="publishedDate")
    news_url: HttpUrl = Field(..., alias="newsURL")
    news_title: str = Field(..., alias="newsTitle")
    news_base_url: str = Field(..., alias="newsBaseURL")
    news_publisher: str = Field(..., alias="newsPublisher")
    new_grade: str = Field(..., alias="newGrade")
    previous_grade: str = Field(..., alias="previousGrade")
    grading_company: str = Field(..., alias="gradingCompany")
    action: str
    price_when_posted: float = Field(..., alias="priceWhenPosted")

    model_config = ConfigDict(populate_by_name=True)
