from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.financial_statements import CompanyBalanceSheetRead
from app.schemas.financial_statements import CompanyCashFlowStatementRead
from app.schemas.company_metrics import CompanyDiscountedCashFlowRead
from app.schemas.quote import CompanyDividendRead, StockPriceRead
from app.schemas.financial_health import CompanyFinancialHealthRead
from app.schemas.financial_statements import CompanyFinancialRatioRead
from app.schemas.market_data import CompanyGradingRead, CompanyGradingSummaryRead
from app.schemas.financial_statements import CompanyIncomeStatementRead
from app.schemas.company_metrics import CompanyKeyMetricsRead
from app.schemas.market_data import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)
from app.schemas.market_data import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.schemas.quote import StockPriceChangeRead
from app.schemas.market_data import CompanyRatingSummaryRead


class Company(BaseModel):
    symbol: str
    company_name: str
    market_cap: float
    currency: str
    exchange_full_name: str
    exchange: str
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    sector: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    image: Optional[str] = None
    ipo_date: Optional[date] = None

    @field_validator("website", "image", mode="before")
    @classmethod
    def convert_url_to_string(cls, v):
        """Convert HttpUrl objects to strings."""
        if v is None:
            return v
        return str(v)


class CompanyRead(Company):
    price: Optional[float] = None
    daily_price_change: Optional[float] = None
    daily_price_change_percent: Optional[float] = None
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanyWrite(Company):
    model_config = ConfigDict(from_attributes=True)


class CompanyPageResponse(BaseModel):
    company: CompanyRead
    grading_summary: Optional[CompanyGradingSummaryRead]
    rating_summary: Optional[CompanyRatingSummaryRead]
    dcf: Optional[CompanyDiscountedCashFlowRead]
    price_target: Optional[CompanyPriceTargetRead]
    stock_prices: List[StockPriceRead]
    price_change: Optional[StockPriceChangeRead]
    price_target_summary: Optional[CompanyPriceTargetSummaryRead]
    latest_gradings: List[CompanyGradingRead] = []
    price_target_news: List[CompanyPriceTargetNewsRead] = []
    general_news: List[CompanyGeneralNewsRead] = []
    grading_news: List[CompanyGradingNewsRead] = []

    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialResponse(BaseModel):
    balance_sheets: List[CompanyBalanceSheetRead] = []
    income_statements: List[CompanyIncomeStatementRead] = []
    cash_flow_statements: List[CompanyCashFlowStatementRead] = []
    key_metrics: List[CompanyKeyMetricsRead] = []
    financial_ratios: List[CompanyFinancialRatioRead] = []
    dividends: List[CompanyDividendRead] = []

    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialHealthResponse(BaseModel):
    company: CompanyRead
    profitability_analysis: List[CompanyFinancialHealthRead] = []
    efficiency_analysis: List[CompanyFinancialHealthRead] = []
    liquidity_and_short_term_solvency: List[CompanyFinancialHealthRead] = []
    leverage_and_capital_structure: List[CompanyFinancialHealthRead] = []
    valuation_and_market_multiples: List[CompanyFinancialHealthRead] = []
    cashflow_strength: List[CompanyFinancialHealthRead] = []
    asset_quality_and_capital_efficiency: List[CompanyFinancialHealthRead] = []
    dividend_and_shareholder_returns: List[CompanyFinancialHealthRead] = []
    per_share_performance: List[CompanyFinancialHealthRead] = []
    tax_and_cost_structure: List[CompanyFinancialHealthRead] = []
    model_config = ConfigDict(from_attributes=True)
