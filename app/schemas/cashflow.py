from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyCashFlowStatement(BaseModel):
    company_id: int
    symbol: str
    date: date_type
    reported_currency: str
    cik: str
    filing_date: date_type
    accepted_date: datetime
    fiscal_year: int
    period: str
    net_income: Optional[int] = None
    depreciation_and_amortization: Optional[int] = None
    deferred_income_tax: Optional[int] = None
    stock_based_compensation: Optional[int] = None
    change_in_working_capital: Optional[int] = None
    accounts_receivables: Optional[int] = None
    inventory: Optional[int] = None
    accounts_payables: Optional[int] = None
    other_working_capital: Optional[int] = None
    other_non_cash_items: Optional[int] = None
    net_cash_provided_by_operating_activities: Optional[int] = None
    investments_in_property_plant_and_equipment: Optional[int] = None
    acquisitions_net: Optional[int] = None
    purchases_of_investments: Optional[int] = None
    sales_maturities_of_investments: Optional[int] = None
    other_investing_activities: Optional[int] = None
    net_cash_provided_by_investing_activities: Optional[int] = None
    net_debt_issuance: Optional[int] = None
    long_term_net_debt_issuance: Optional[int] = None
    short_term_net_debt_issuance: Optional[int] = None
    net_stock_issuance: Optional[int] = None
    net_common_stock_issuance: Optional[int] = None
    common_stock_issuance: Optional[int] = None
    common_stock_repurchased: Optional[int] = None
    net_preferred_stock_issuance: Optional[int] = None
    net_dividends_paid: Optional[int] = None
    common_dividends_paid: Optional[int] = None
    preferred_dividends_paid: Optional[int] = None
    other_financing_activities: Optional[int] = None
    net_cash_provided_by_financing_activities: Optional[int] = None
    effect_of_forex_changes_on_cash: Optional[int] = None
    net_change_in_cash: Optional[int] = None
    cash_at_end_of_period: Optional[int] = None
    cash_at_beginning_of_period: Optional[int] = None
    operating_cash_flow: Optional[int] = None
    capital_expenditure: Optional[int] = None
    free_cash_flow: Optional[int] = None
    income_taxes_paid: Optional[int] = None
    interest_paid: Optional[int] = None


class CompanyCashFlowStatementWrite(CompanyCashFlowStatement):
    model_config = ConfigDict(from_attributes=True)


class CompanyCashFlowStatementRead(CompanyCashFlowStatement):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
