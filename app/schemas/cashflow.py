from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyCashFlowStatement(BaseModel):
    company_id: int
    symbol: str
    date: str
    reported_currency: str
    cik: str
    filing_date: str
    accepted_date: str
    fiscal_year: str
    period: str
    net_income: int
    depreciation_and_amortization: int
    deferred_income_tax: int
    stock_based_compensation: int
    change_in_working_capital: int
    accounts_receivables: int
    inventory: int
    accounts_payables: int
    other_working_capital: int
    other_non_cash_items: int
    net_cash_provided_by_operating_activities: int
    investments_in_property_plant_and_equipment: int
    acquisitions_net: int
    purchases_of_investments: int
    sales_maturities_of_investments: int
    other_investing_activities: int
    net_cash_provided_by_investing_activities: int
    net_debt_issuance: int
    long_term_net_debt_issuance: int
    short_term_net_debt_issuance: int
    net_stock_issuance: int
    net_common_stock_issuance: int
    common_stock_issuance: int
    common_stock_repurchased: int
    net_preferred_stock_issuance: int
    net_dividends_paid: int
    common_dividends_paid: int
    preferred_dividends_paid: int
    other_financing_activities: int
    net_cash_provided_by_financing_activities: int
    effect_of_forex_changes_on_cash: int
    net_change_in_cash: int
    cash_at_end_of_period: int
    cash_at_beginning_of_period: int
    operating_cash_flow: int
    capital_expenditure: int
    free_cash_flow: int
    income_taxes_paid: int
    interest_paid: int


class CompanyCashFlowStatementWrite(CompanyCashFlowStatement):
    model_config = ConfigDict(from_attributes=True)


class CompanyCashFlowStatementRead(BaseModel):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
