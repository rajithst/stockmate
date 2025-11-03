from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyBalanceSheet(BaseModel):
    company_id: int
    symbol: str
    date: date_type
    reported_currency: str
    cik: str
    filing_date: date_type
    accepted_date: datetime
    fiscal_year: int
    period: str
    cash_and_cash_equivalents: Optional[int] = None
    short_term_investments: Optional[int] = None
    cash_and_short_term_investments: Optional[int] = None
    net_receivables: Optional[int] = None
    accounts_receivables: Optional[int] = None
    other_receivables: Optional[int] = None
    inventory: Optional[int] = None
    prepaids: Optional[int] = None
    other_current_assets: Optional[int] = None
    total_current_assets: Optional[int] = None
    property_plant_equipment_net: Optional[int] = None
    goodwill: Optional[int] = None
    intangible_assets: Optional[int] = None
    goodwill_and_intangible_assets: Optional[int] = None
    long_term_investments: Optional[int] = None
    tax_assets: Optional[int] = None
    other_non_current_assets: Optional[int] = None
    total_non_current_assets: Optional[int] = None
    other_assets: Optional[int] = None
    total_assets: Optional[int] = None
    total_payables: Optional[int] = None
    account_payables: Optional[int] = None
    other_payables: Optional[int] = None
    accrued_expenses: Optional[int] = None
    short_term_debt: Optional[int] = None
    capital_lease_obligations_current: Optional[int] = None
    tax_payables: Optional[int] = None
    deferred_revenue: Optional[int] = None
    other_current_liabilities: Optional[int] = None
    total_current_liabilities: Optional[int] = None
    long_term_debt: Optional[int] = None
    deferred_revenue_non_current: Optional[int] = None
    deferred_tax_liabilities_non_current: Optional[int] = None
    other_non_current_liabilities: Optional[int] = None
    total_non_current_liabilities: Optional[int] = None
    other_liabilities: Optional[int] = None
    capital_lease_obligations: Optional[int] = None
    total_liabilities: Optional[int] = None
    treasury_stock: Optional[int] = None
    preferred_stock: Optional[int] = None
    common_stock: Optional[int] = None
    retained_earnings: Optional[int] = None
    additional_paid_in_capital: Optional[int] = None
    accumulated_other_comprehensive_income_loss: Optional[int] = None
    other_total_stockholders_equity: Optional[int] = None
    total_stockholders_equity: Optional[int] = None
    total_equity: Optional[int] = None
    minority_interest: Optional[int] = None
    total_liabilities_and_total_equity: Optional[int] = None
    total_investments: Optional[int] = None
    total_debt: Optional[int] = None
    net_debt: Optional[int] = None


class CompanyBalanceSheetWrite(CompanyBalanceSheet):
    model_config = ConfigDict(from_attributes=True)


class CompanyBalanceSheetRead(CompanyBalanceSheet):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
