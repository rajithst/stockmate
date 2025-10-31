from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.balance_sheet import CompanyBalanceSheetRead
from app.schemas.cashflow import CompanyCashFlowStatementRead
from app.schemas.dcf import DiscountedCashFlowRead
from app.schemas.dividend import CompanyDividendRead
from app.schemas.financial_health import CompanyFinancialHealthRead
from app.schemas.financial_ratio import CompanyFinancialRatioRead
from app.schemas.grading import CompanyGradingRead, CompanyGradingSummaryRead
from app.schemas.income_statement import CompanyIncomeStatementRead
from app.schemas.key_metrics import CompanyKeyMetricsRead
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)
from app.schemas.price_target import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.schemas.quote import StockPriceChangeRead
from app.schemas.rating import CompanyRatingSummaryRead


class Company(BaseModel):
    symbol: str
    company_name: str
    price: float
    price_change: float
    price_change_percent: float
    market_cap: float
    currency: str
    exchange_full_name: str
    exchange: str
    industry: str
    website: str
    description: str
    sector: str
    country: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    image: str
    ipo_date: str

    @field_validator("website", "image", mode="before")
    @classmethod
    def convert_url_to_string(cls, v):
        """Convert HttpUrl objects to strings."""
        if v is None:
            return v
        return str(v)


class CompanyRead(Company):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanyWrite(Company):
    model_config = ConfigDict(from_attributes=True)


class CompanyPageResponse(BaseModel):
    company: CompanyRead
    grading_summary: Optional[CompanyGradingSummaryRead]
    rating_summary: Optional[CompanyRatingSummaryRead]
    dcf: Optional[DiscountedCashFlowRead]
    price_target: Optional[CompanyPriceTargetRead]
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
    profitability: List[CompanyFinancialHealthRead] = []
    efficiency: List[CompanyFinancialHealthRead] = []
    liquidity_and_solvency: List[CompanyFinancialHealthRead] = []
    cashflow_strength: List[CompanyFinancialHealthRead] = []
    valuation: List[CompanyFinancialHealthRead] = []
    growth_and_investment: List[CompanyFinancialHealthRead] = []
    dividend_and_shareholder_return: List[CompanyFinancialHealthRead] = []

    model_config = ConfigDict(from_attributes=True)
