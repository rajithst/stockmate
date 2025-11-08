"""
Consolidated market data schemas:
- CompanyGrading: Individual grading events
- CompanyGradingSummary: Summary of analyst gradings
- CompanyRatingSummary: Analyst rating summaries with various score components
- CompanyPriceTarget: Price target data
- CompanyPriceTargetSummary: Summary of price targets
- CompanyStockNews: Stock-related news
- CompanyGeneralNews: General company news
- CompanyPriceTargetNews: News related to price targets
- CompanyGradingNews: News related to grading changes
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ========================
# GRADING SCHEMAS
# ========================


class CompanyGrading(BaseModel):
    symbol: str
    date: datetime
    grading_company: Optional[str] = None
    previous_grade: Optional[str] = None
    new_grade: Optional[str] = None
    action: Optional[str] = None


class CompanyGradingWrite(CompanyGrading):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyGradingRead(CompanyGrading):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyGradingSummary(BaseModel):
    symbol: str
    buy: int
    hold: int
    sell: int
    strong_buy: int
    strong_sell: int
    consensus: str


class CompanyGradingSummaryRead(CompanyGradingSummary):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyGradingSummaryWrite(CompanyGradingSummary):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


# ========================
# RATING SCHEMAS
# ========================


class CompanyRatingSummary(BaseModel):
    symbol: str
    rating: Optional[str] = None
    overall_score: Optional[int] = None
    discounted_cash_flow_score: Optional[int] = None
    return_on_equity_score: Optional[int] = None
    return_on_assets_score: Optional[int] = None
    debt_to_equity_score: Optional[int] = None
    price_to_earnings_score: Optional[int] = None
    price_to_book_score: Optional[int] = None


class CompanyRatingSummaryRead(CompanyRatingSummary):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyRatingSummaryWrite(CompanyRatingSummary):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


# ========================
# PRICE TARGET SCHEMAS
# ========================


class CompanyPriceTarget(BaseModel):
    symbol: str
    target_high: Optional[float] = None
    target_low: Optional[float] = None
    target_consensus: Optional[float] = None
    target_median: Optional[float] = None


class CompanyPriceTargetRead(CompanyPriceTarget):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetWrite(CompanyPriceTarget):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetSummary(BaseModel):
    symbol: str
    last_month_count: int
    last_month_average_price_target: float
    last_quarter_count: int
    last_quarter_average_price_target: float
    last_year_count: int
    last_year_average_price_target: float
    all_time_count: int
    all_time_average_price_target: float
    publishers: Optional[str] = None


class CompanyPriceTargetSummaryRead(CompanyPriceTargetSummary):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetSummaryWrite(CompanyPriceTargetSummary):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


# ========================
# NEWS SCHEMAS
# ========================


class CompanyStockNews(BaseModel):
    symbol: Optional[str] = None
    published_date: datetime
    publisher: str
    news_title: str
    news_url: str
    text: str
    image: Optional[str] = None
    site: Optional[str] = None
    sentiment: Optional[str] = None


class CompanyStockNewsRead(CompanyStockNews):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyStockNewsWrite(CompanyStockNews):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyGeneralNews(BaseModel):
    symbol: Optional[str] = None
    published_date: datetime
    publisher: str
    news_title: str
    news_url: str
    text: str
    image: Optional[str] = None
    site: Optional[str] = None
    sentiment: Optional[str] = None


class CompanyGeneralNewsRead(CompanyGeneralNews):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyGeneralNewsWrite(CompanyGeneralNews):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetNews(BaseModel):
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
    sentiment: Optional[str] = None


class CompanyPriceTargetNewsWrite(CompanyPriceTargetNews):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyPriceTargetNewsRead(CompanyPriceTargetNews):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyGradingNews(BaseModel):
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
    sentiment: Optional[str] = None


class CompanyGradingNewsWrite(CompanyGradingNews):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyGradingNewsRead(CompanyGradingNews):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
