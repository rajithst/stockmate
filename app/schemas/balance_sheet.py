from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompanyBalanceSheet(BaseModel):
    company_id: int
    symbol: str
    date: str
    reported_currency: str
    cik: str
    filing_date: str
    accepted_date: str
    fiscal_year: str
    period: str
    cash_and_cash_equivalents: int
    short_term_investments: int
    cash_and_short_term_investments: int
    net_receivables: int
    accounts_receivables: int
    other_receivables: int
    inventory: int
    prepaids: int
    other_current_assets: int
    total_current_assets: int
    property_plant_equipment_net: int
    goodwill: int
    intangible_assets: int
    goodwill_and_intangible_assets: int
    long_term_investments: int
    tax_assets: int
    other_non_current_assets: int
    total_non_current_assets: int
    other_assets: int
    total_assets: int
    total_payables: int
    account_payables: int
    other_payables: int
    accrued_expenses: int
    short_term_debt: int
    capital_lease_obligations_current: int
    tax_payables: int
    deferred_revenue: int
    other_current_liabilities: int
    total_current_liabilities: int
    long_term_debt: int
    deferred_revenue_non_current: int
    deferred_tax_liabilities_non_current: int
    other_non_current_liabilities: int
    total_non_current_liabilities: int
    other_liabilities: int
    capital_lease_obligations: int
    total_liabilities: int
    treasury_stock: int
    preferred_stock: int
    common_stock: int
    retained_earnings: int
    additional_paid_in_capital: int
    accumulated_other_comprehensive_income_loss: int
    other_total_stockholders_equity: int
    total_stockholders_equity: int
    total_equity: int
    minority_interest: int
    total_liabilities_and_total_equity: int
    total_investments: int
    total_debt: int
    net_debt: int


class CompanyBalanceSheetWrite(CompanyBalanceSheet):
    model_config = ConfigDict(from_attributes=True)


class CompanyBalanceSheetRead(CompanyBalanceSheet):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
