"""
Consolidated company metrics schemas:
- CompanyAnalystEstimate: Analyst forecasts (revenue, EBITDA, EPS)
- CompanyKeyMetrics: Market caps, EV ratios, ROA/ROE/ROIC, efficiency metrics
- CompanyDiscountedCashFlow: DCF valuation (dcf value, stock price)
- CompanyRevenueProductSegmentation: Revenue breakdown by product/business segment
"""

from datetime import date as date_type, datetime
from typing import Optional
import json

from pydantic import BaseModel, ConfigDict, field_validator


# ========================
# ANALYST ESTIMATE SCHEMAS
# ========================


class CompanyAnalystEstimate(BaseModel):
    symbol: str
    date: date_type

    # Revenue estimates (in millions)
    revenue_low: Optional[float] = None
    revenue_high: Optional[float] = None
    revenue_avg: Optional[float] = None

    # EBITDA estimates (in millions)
    ebitda_low: Optional[float] = None
    ebitda_high: Optional[float] = None
    ebitda_avg: Optional[float] = None

    # EBIT estimates (in millions)
    ebit_low: Optional[float] = None
    ebit_high: Optional[float] = None
    ebit_avg: Optional[float] = None

    # Net income estimates (in millions)
    net_income_low: Optional[float] = None
    net_income_high: Optional[float] = None
    net_income_avg: Optional[float] = None

    # SGA expense estimates (in millions)
    sga_expense_low: Optional[float] = None
    sga_expense_high: Optional[float] = None
    sga_expense_avg: Optional[float] = None

    # EPS estimates
    eps_avg: Optional[float] = None
    eps_high: Optional[float] = None
    eps_low: Optional[float] = None

    # Number of analysts
    num_analysts_revenue: Optional[int] = None
    num_analysts_eps: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyAnalystEstimateWrite(CompanyAnalystEstimate):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyAnalystEstimateRead(CompanyAnalystEstimate):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# KEY METRICS SCHEMAS
# ========================


class CompanyKeyMetrics(BaseModel):
    symbol: str
    date: date_type
    fiscal_year: int
    period: str
    reported_currency: str
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    ev_to_sales: Optional[float] = None
    ev_to_operating_cash_flow: Optional[float] = None
    ev_to_free_cash_flow: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    net_debt_to_ebitda: Optional[float] = None
    current_ratio: Optional[float] = None
    income_quality: Optional[float] = None
    graham_number: Optional[float] = None
    graham_net_net: Optional[float] = None
    tax_burden: Optional[float] = None
    interest_burden: Optional[float] = None
    working_capital: Optional[float] = None
    invested_capital: Optional[float] = None
    return_on_assets: Optional[float] = None
    operating_return_on_assets: Optional[float] = None
    return_on_tangible_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_invested_capital: Optional[float] = None
    return_on_capital_employed: Optional[float] = None
    earnings_yield: Optional[float] = None
    free_cash_flow_yield: Optional[float] = None
    capex_to_operating_cash_flow: Optional[float] = None
    capex_to_depreciation: Optional[float] = None
    capex_to_revenue: Optional[float] = None
    sales_general_and_administrative_to_revenue: Optional[float] = None
    research_and_development_to_revenue: Optional[float] = None
    stock_based_compensation_to_revenue: Optional[float] = None
    intangibles_to_total_assets: Optional[float] = None
    average_receivables: Optional[float] = None
    average_payables: Optional[float] = None
    average_inventory: Optional[float] = None
    days_of_sales_outstanding: Optional[float] = None
    days_of_payables_outstanding: Optional[float] = None
    days_of_inventory_outstanding: Optional[float] = None
    operating_cycle: Optional[float] = None
    cash_conversion_cycle: Optional[float] = None
    free_cash_flow_to_equity: Optional[float] = None
    free_cash_flow_to_firm: Optional[float] = None
    tangible_asset_value: Optional[float] = None
    net_current_asset_value: Optional[float] = None


class CompanyKeyMetricsWrite(CompanyKeyMetrics):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyKeyMetricsRead(CompanyKeyMetrics):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# DISCOUNTED CASH FLOW SCHEMAS
# ========================


class CompanyDiscountedCashFlow(BaseModel):
    symbol: str
    date: date_type
    dcf: float
    stock_price: Optional[float] = None


class CompanyDiscountedCashFlowRead(CompanyDiscountedCashFlow):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyDiscountedCashFlowWrite(CompanyDiscountedCashFlow):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


# ========================
# REVENUE PRODUCT SEGMENTATION SCHEMAS
# ========================


class CompanyRevenueProductSegmentation(BaseModel):
    symbol: str
    fiscal_year: int
    period: str
    date: date_type
    segments_data: str  # JSON string: Product segment names and revenue values
    reported_currency: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("segments_data", mode="before")
    @classmethod
    def serialize_segments_data(cls, v):
        """Convert dict to JSON string if needed."""
        if isinstance(v, dict):
            return json.dumps(v)
        return v


class CompanyRevenueProductSegmentationWrite(CompanyRevenueProductSegmentation):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyRevenueProductSegmentationRead(CompanyRevenueProductSegmentation):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
