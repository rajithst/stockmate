from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.financial_statements import CompanyBalanceSheetRead
from app.schemas.financial_statements import CompanyCashFlowStatementRead
from app.schemas.company_metrics import (
    CompanyDiscountedCashFlowRead,
    CompanyAnalystEstimateRead,
)
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
    is_in_db: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanyWrite(Company):
    model_config = ConfigDict(from_attributes=True)


class CompanyInsight(BaseModel):
    year: int
    quarter: str
    value: float


class CompanyPageResponse(BaseModel):
    company: CompanyRead
    ratios: CompanyFinancialRatioRead
    grading_summary: Optional[CompanyGradingSummaryRead]
    rating_summary: Optional[CompanyRatingSummaryRead]
    dcf: Optional[CompanyDiscountedCashFlowRead]
    price_target: Optional[CompanyPriceTargetRead]
    stock_prices: List[StockPriceRead]
    price_change: Optional[StockPriceChangeRead]
    price_target_summary: Optional[CompanyPriceTargetSummaryRead]
    analyst_estimates: List[CompanyAnalystEstimateRead] = []
    latest_gradings: List[CompanyGradingRead] = []
    price_target_news: List[CompanyPriceTargetNewsRead] = []
    general_news: List[CompanyGeneralNewsRead] = []
    grading_news: List[CompanyGradingNewsRead] = []

    model_config = ConfigDict(from_attributes=True)


class CompanyInsightsResponse(BaseModel):
    net_income: list[CompanyInsight]
    gross_profit_margin: list[CompanyInsight]
    operating_profit_margin: list[CompanyInsight]
    ebita: list[CompanyInsight]
    free_cash_flow: list[CompanyInsight]
    eps: list[CompanyInsight]
    eps_diluted: list[CompanyInsight]
    weighted_average_shs_out: list[CompanyInsight]
    return_on_equity: list[CompanyInsight]
    debt_to_equity_ratio: list[CompanyInsight]
    total_debt: list[CompanyInsight]
    operating_cash_flow: list[CompanyInsight]
    market_cap: list[CompanyInsight]
    dividend_yield: list[CompanyInsight]

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


class NonUSCompany(BaseModel):
    """Base schema for non-US company data from YFinance"""

    symbol: str
    short_name: Optional[str] = None
    long_name: Optional[str] = None
    quote_type: str = "EQUITY"
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    zip: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    ir_website: Optional[str] = None
    industry: Optional[str] = None
    industry_key: Optional[str] = None
    industry_display: Optional[str] = None
    sector: Optional[str] = None
    sector_key: Optional[str] = None
    sector_display: Optional[str] = None
    long_business_summary: Optional[str] = None
    description: Optional[str] = None
    full_time_employees: Optional[float] = None
    image: Optional[str] = None
    default_image: Optional[bool] = None
    exchange: Optional[str] = None
    full_exchange_name: Optional[str] = None
    exchange_timezone_name: Optional[str] = None
    exchange_timezone_short_name: Optional[str] = None
    gmt_offset_milliseconds: Optional[float] = None
    market: Optional[str] = None
    market_state: Optional[str] = None
    ipo_date: Optional[date] = None
    first_trade_date_milliseconds: Optional[float] = None
    tradeable: Optional[bool] = None
    crypto_tradeable: Optional[bool] = None
    currency: Optional[str] = None
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    open: Optional[float] = None
    day_low: Optional[float] = None
    day_high: Optional[float] = None
    regular_market_previous_close: Optional[float] = None
    regular_market_open: Optional[float] = None
    regular_market_day_low: Optional[float] = None
    regular_market_day_high: Optional[float] = None
    regular_market_price: Optional[float] = None
    regular_market_change: Optional[float] = None
    regular_market_change_percent: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    bid_size: Optional[float] = None
    ask_size: Optional[float] = None
    price_hint: Optional[float] = None
    volume: Optional[float] = None
    regular_market_volume: Optional[float] = None
    average_volume: Optional[float] = None
    average_volume_10_days: Optional[float] = None
    average_daily_volume_10_day: Optional[float] = None
    average_daily_volume_3_month: Optional[float] = None
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    shares_outstanding: Optional[float] = None
    implied_shares_outstanding: Optional[float] = None
    float_shares: Optional[float] = None
    held_percent_insiders: Optional[float] = None
    held_percent_institutions: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low_change: Optional[float] = None
    fifty_two_week_low_change_percent: Optional[float] = None
    fifty_two_week_high_change: Optional[float] = None
    fifty_two_week_high_change_percent: Optional[float] = None
    fifty_two_week_range: Optional[str] = None
    fifty_two_week_change: Optional[float] = None
    fifty_two_week_change_percent: Optional[float] = None
    all_time_high: Optional[float] = None
    all_time_low: Optional[float] = None
    fifty_day_average: Optional[float] = None
    fifty_day_average_change: Optional[float] = None
    fifty_day_average_change_percent: Optional[float] = None
    two_hundred_day_average: Optional[float] = None
    two_hundred_day_average_change: Optional[float] = None
    two_hundred_day_average_change_percent: Optional[float] = None
    dividend_rate: Optional[float] = None
    dividend_yield: Optional[float] = None
    trailing_annual_dividend_rate: Optional[float] = None
    trailing_annual_dividend_yield: Optional[float] = None
    five_year_avg_dividend_yield: Optional[float] = None
    ex_dividend_date: Optional[float] = None
    last_dividend_date: Optional[float] = None
    last_dividend_value: Optional[float] = None
    payout_ratio: Optional[float] = None
    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    trailing_peg_ratio: Optional[float] = None
    price_to_sales_trailing_12_months: Optional[float] = None
    price_to_book: Optional[float] = None
    enterprise_to_revenue: Optional[float] = None
    trailing_eps: Optional[float] = None
    forward_eps: Optional[float] = None
    eps_trailing_twelve_months: Optional[float] = None
    eps_for_forward: Optional[float] = None
    earnings_growth: Optional[float] = None
    earnings_quarterly_growth: Optional[float] = None
    net_income_to_common: Optional[float] = None
    book_value: Optional[float] = None
    total_cash: Optional[float] = None
    total_cash_per_share: Optional[float] = None
    total_debt: Optional[float] = None
    total_revenue: Optional[float] = None
    revenue_per_share: Optional[float] = None
    gross_profits: Optional[float] = None
    beta: Optional[float] = None
    profit_margins: Optional[float] = None
    gross_margins: Optional[float] = None
    operating_margins: Optional[float] = None
    ebitda_margins: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    revenue_growth: Optional[float] = None
    number_of_analyst_opinions: Optional[float] = None
    recommendation_key: Optional[str] = None
    recommendation_mean: Optional[float] = None
    average_analyst_rating: Optional[str] = None
    target_mean_price: Optional[float] = None
    target_median_price: Optional[float] = None
    target_high_price: Optional[float] = None
    target_low_price: Optional[float] = None
    last_fiscal_year_end: Optional[int] = None
    next_fiscal_year_end: Optional[int] = None
    most_recent_quarter: Optional[int] = None
    earnings_timestamp: Optional[int] = None
    earnings_timestamp_start: Optional[int] = None
    earnings_timestamp_end: Optional[int] = None
    earnings_call_timestamp_start: Optional[int] = None
    earnings_call_timestamp_end: Optional[int] = None
    is_earnings_date_estimate: Optional[bool] = None
    last_split_factor: Optional[str] = None
    last_split_date: Optional[int] = None
    audit_risk: Optional[int] = None
    board_risk: Optional[int] = None
    compensation_risk: Optional[int] = None
    share_holder_rights_risk: Optional[int] = None
    overall_risk: Optional[int] = None
    governance_epoch_date: Optional[int] = None
    compensation_as_of_epoch_date: Optional[int] = None
    quote_source_name: Optional[str] = None
    triggerable: Optional[bool] = None
    custom_price_alert_confidence: Optional[str] = None
    source_interval: Optional[int] = None
    exchange_data_delayed_by: Optional[int] = None
    message_board_id: Optional[str] = None
    has_pre_post_market_data: Optional[bool] = None
    esg_populated: Optional[bool] = None
    region: Optional[str] = None
    language: Optional[str] = None
    type_display: Optional[str] = None
    regular_market_day_range: Optional[str] = None
    regular_market_time: Optional[int] = None
    sand_p_52_week_change: Optional[float] = None
    max_age: Optional[int] = None

    @field_validator("website", "ir_website", "image", mode="before")
    @classmethod
    def convert_url_to_string(cls, v):
        """Convert HttpUrl objects to strings."""
        if v is None:
            return v
        return str(v)


class NonUSCompanyRead(NonUSCompany):
    """Read schema for non-US company with database metadata"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NonUSCompanyWrite(NonUSCompany):
    """Write schema for non-US company"""

    model_config = ConfigDict(from_attributes=True)
