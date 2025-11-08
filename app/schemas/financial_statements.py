"""
Consolidated financial statement schemas:
- CompanyIncomeStatement: Revenue, expenses, profit metrics
- CompanyBalanceSheet: Assets, liabilities, equity
- CompanyCashFlowStatement: Operating, investing, financing cash flows
- CompanyFinancialRatio: 100+ calculated financial ratios
"""

from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ========================
# INCOME STATEMENT SCHEMAS
# ========================


class CompanyIncomeStatement(BaseModel):
    symbol: str
    date: date_type
    reported_currency: str
    cik: str
    filing_date: date_type
    accepted_date: datetime
    fiscal_year: int
    period: str
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    research_and_development_expenses: Optional[float] = None
    general_and_administrative_expenses: Optional[float] = None
    selling_and_marketing_expenses: Optional[float] = None
    selling_general_and_administrative_expenses: Optional[float] = None
    other_expenses: Optional[float] = None
    operating_expenses: Optional[float] = None
    cost_and_expenses: Optional[float] = None
    net_interest_income: Optional[float] = None
    interest_income: Optional[float] = None
    interest_expense: Optional[float] = None
    depreciation_and_amortization: Optional[float] = None
    ebitda: Optional[float] = None
    ebit: Optional[float] = None
    non_operating_income_excluding_interest: Optional[float] = None
    operating_income: Optional[float] = None
    total_other_income_expenses_net: Optional[float] = None
    income_before_tax: Optional[float] = None
    income_tax_expense: Optional[float] = None
    net_income_from_continuing_operations: Optional[float] = None
    net_income_from_discontinued_operations: Optional[float] = None
    other_adjustments_to_net_income: Optional[float] = None
    net_income: Optional[float] = None
    net_income_deductions: Optional[float] = None
    bottom_line_net_income: Optional[float] = None
    eps: Optional[float] = None
    eps_diluted: Optional[float] = None
    weighted_average_shs_out: Optional[float] = None
    weighted_average_shs_out_dil: Optional[float] = None


class CompanyIncomeStatementWrite(CompanyIncomeStatement):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyIncomeStatementRead(CompanyIncomeStatement):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# BALANCE SHEET SCHEMAS
# ========================


class CompanyBalanceSheet(BaseModel):
    symbol: str
    date: date_type
    reported_currency: str
    cik: str
    filing_date: date_type
    accepted_date: datetime
    fiscal_year: int
    period: str
    cash_and_cash_equivalents: Optional[float] = None
    short_term_investments: Optional[float] = None
    cash_and_short_term_investments: Optional[float] = None
    net_receivables: Optional[float] = None
    accounts_receivables: Optional[float] = None
    other_receivables: Optional[float] = None
    inventory: Optional[float] = None
    prepaids: Optional[float] = None
    other_current_assets: Optional[float] = None
    total_current_assets: Optional[float] = None
    property_plant_equipment_net: Optional[float] = None
    goodwill: Optional[float] = None
    intangible_assets: Optional[float] = None
    goodwill_and_intangible_assets: Optional[float] = None
    long_term_investments: Optional[float] = None
    tax_assets: Optional[float] = None
    other_non_current_assets: Optional[float] = None
    total_non_current_assets: Optional[float] = None
    other_assets: Optional[float] = None
    total_assets: Optional[float] = None
    total_payables: Optional[float] = None
    account_payables: Optional[float] = None
    other_payables: Optional[float] = None
    accrued_expenses: Optional[float] = None
    short_term_debt: Optional[float] = None
    capital_lease_obligations_current: Optional[float] = None
    tax_payables: Optional[float] = None
    deferred_revenue: Optional[float] = None
    other_current_liabilities: Optional[float] = None
    total_current_liabilities: Optional[float] = None
    long_term_debt: Optional[float] = None
    deferred_revenue_non_current: Optional[float] = None
    deferred_tax_liabilities_non_current: Optional[float] = None
    other_non_current_liabilities: Optional[float] = None
    total_non_current_liabilities: Optional[float] = None
    other_liabilities: Optional[float] = None
    capital_lease_obligations: Optional[float] = None
    total_liabilities: Optional[float] = None
    treasury_stock: Optional[float] = None
    preferred_stock: Optional[float] = None
    common_stock: Optional[float] = None
    retained_earnings: Optional[float] = None
    additional_paid_in_capital: Optional[float] = None
    accumulated_other_comprehensive_income_loss: Optional[float] = None
    other_total_stockholders_equity: Optional[float] = None
    total_stockholders_equity: Optional[float] = None
    total_equity: Optional[float] = None
    minority_interest: Optional[float] = None
    total_liabilities_and_total_equity: Optional[float] = None
    total_investments: Optional[float] = None
    total_debt: Optional[float] = None
    net_debt: Optional[float] = None


class CompanyBalanceSheetWrite(CompanyBalanceSheet):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyBalanceSheetRead(CompanyBalanceSheet):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ========================
# CASH FLOW STATEMENT SCHEMAS
# ========================


class CompanyCashFlowStatement(BaseModel):
    symbol: str
    date: date_type
    reported_currency: str
    cik: str
    filing_date: date_type
    accepted_date: datetime
    fiscal_year: int
    period: str
    net_income: Optional[float] = None
    depreciation_and_amortization: Optional[float] = None
    deferred_income_tax: Optional[float] = None
    stock_based_compensation: Optional[float] = None
    change_in_working_capital: Optional[float] = None
    accounts_receivables: Optional[float] = None
    inventory: Optional[float] = None
    accounts_payables: Optional[float] = None
    other_working_capital: Optional[float] = None
    other_non_cash_items: Optional[float] = None
    net_cash_provided_by_operating_activities: Optional[float] = None
    investments_in_property_plant_and_equipment: Optional[float] = None
    acquisitions_net: Optional[float] = None
    purchases_of_investments: Optional[float] = None
    sales_maturities_of_investments: Optional[float] = None
    other_investing_activities: Optional[float] = None
    net_cash_provided_by_investing_activities: Optional[float] = None
    net_debt_issuance: Optional[float] = None
    long_term_net_debt_issuance: Optional[float] = None
    short_term_net_debt_issuance: Optional[float] = None
    net_stock_issuance: Optional[float] = None
    net_common_stock_issuance: Optional[float] = None
    common_stock_issuance: Optional[float] = None
    common_stock_repurchased: Optional[float] = None
    net_preferred_stock_issuance: Optional[float] = None
    net_dividends_paid: Optional[float] = None
    common_dividends_paid: Optional[float] = None
    preferred_dividends_paid: Optional[float] = None
    other_financing_activities: Optional[float] = None
    net_cash_provided_by_financing_activities: Optional[float] = None
    effect_of_forex_changes_on_cash: Optional[float] = None
    net_change_in_cash: Optional[float] = None
    cash_at_end_of_period: Optional[float] = None
    cash_at_beginning_of_period: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    free_cash_flow: Optional[float] = None
    income_taxes_paid: Optional[float] = None
    interest_paid: Optional[float] = None


class CompanyCashFlowStatementWrite(CompanyCashFlowStatement):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyCashFlowStatementRead(CompanyCashFlowStatement):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ========================
# FINANCIAL RATIO SCHEMAS
# ========================


class CompanyFinancialRatio(BaseModel):
    symbol: str
    date: Optional[date_type] = None
    fiscal_year: Optional[int] = None
    period: Optional[str] = None
    reported_currency: Optional[str] = None

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
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyFinancialRatioRead(CompanyFinancialRatio):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
