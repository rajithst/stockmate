from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyKeyMetrics(BaseModel):
    company_id: int
    symbol: str
    date: str
    fiscal_year: str
    period: str
    reported_currency: str
    market_cap: Optional[int] = None
    enterprise_value: Optional[int] = None
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
    working_capital: Optional[int] = None
    invested_capital: Optional[int] = None
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
    average_receivables: Optional[int] = None
    average_payables: Optional[int] = None
    average_inventory: Optional[int] = None
    days_of_sales_outstanding: Optional[float] = None
    days_of_payables_outstanding: Optional[float] = None
    days_of_inventory_outstanding: Optional[float] = None
    operating_cycle: Optional[float] = None
    cash_conversion_cycle: Optional[float] = None
    free_cash_flow_to_equity: Optional[float] = None
    free_cash_flow_to_firm: Optional[float] = None
    tangible_asset_value: Optional[int] = None
    net_current_asset_value: Optional[int] = None


class CompanyKeyMetricsWrite(CompanyKeyMetrics):
    model_config = ConfigDict(from_attributes=True)


class CompanyKeyMetricsRead(CompanyKeyMetrics):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
