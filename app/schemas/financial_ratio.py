from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyFinancialRatio(BaseModel):
    company_id: int
    symbol: str
    date: date_type
    fiscal_year: int
    period: str
    reported_currency: str

    # Profitability margins
    gross_profit_margin: Optional[float] = None
    ebit_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None
    operating_profit_margin: Optional[float] = None
    pretax_profit_margin: Optional[float] = None
    continuous_operations_profit_margin: Optional[float] = None
    net_profit_margin: Optional[float] = None
    bottom_line_profit_margin: Optional[float] = None

    # Efficiency ratios
    receivables_turnover: Optional[float] = None
    payables_turnover: Optional[float] = None
    inventory_turnover: Optional[float] = None
    fixed_asset_turnover: Optional[float] = None
    asset_turnover: Optional[float] = None

    # Liquidity ratios
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    solvency_ratio: Optional[float] = None
    cash_ratio: Optional[float] = None

    # Valuation ratios
    price_to_earnings_ratio: Optional[float] = None
    price_to_earnings_growth_ratio: Optional[float] = None
    forward_price_to_earnings_growth_ratio: Optional[float] = None
    price_to_book_ratio: Optional[float] = None
    price_to_sales_ratio: Optional[float] = None
    price_to_free_cash_flow_ratio: Optional[float] = None
    price_to_operating_cash_flow_ratio: Optional[float] = None

    # Leverage ratios
    debt_to_assets_ratio: Optional[float] = None
    debt_to_equity_ratio: Optional[float] = None
    debt_to_capital_ratio: Optional[float] = None
    long_term_debt_to_capital_ratio: Optional[float] = None
    financial_leverage_ratio: Optional[float] = None

    # Cash flow coverage ratios
    working_capital_turnover_ratio: Optional[float] = None
    operating_cash_flow_ratio: Optional[float] = None
    operating_cash_flow_sales_ratio: Optional[float] = None
    free_cash_flow_operating_cash_flow_ratio: Optional[float] = None
    debt_service_coverage_ratio: Optional[float] = None
    interest_coverage_ratio: Optional[float] = None
    short_term_operating_cash_flow_coverage_ratio: Optional[float] = None
    operating_cash_flow_coverage_ratio: Optional[float] = None
    capital_expenditure_coverage_ratio: Optional[float] = None
    dividend_paid_and_capex_coverage_ratio: Optional[float] = None

    # Dividend ratios
    dividend_payout_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    dividend_yield_percentage: Optional[float] = None

    # Per share metrics
    revenue_per_share: Optional[float] = None
    net_income_per_share: Optional[float] = None
    interest_debt_per_share: Optional[float] = None
    cash_per_share: Optional[float] = None
    book_value_per_share: Optional[float] = None
    tangible_book_value_per_share: Optional[float] = None
    shareholders_equity_per_share: Optional[float] = None
    operating_cash_flow_per_share: Optional[float] = None
    capex_per_share: Optional[float] = None
    free_cash_flow_per_share: Optional[float] = None

    # Misc ratios
    net_income_per_ebt: Optional[float] = None
    ebt_per_ebit: Optional[float] = None
    price_to_fair_value: Optional[float] = None
    debt_to_market_cap: Optional[float] = None
    effective_tax_rate: Optional[float] = None
    enterprise_value_multiple: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialRatioWrite(CompanyFinancialRatio):
    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialRatioRead(CompanyFinancialRatio):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
