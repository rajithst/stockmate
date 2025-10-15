from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyIncomeStatement(BaseModel):
    company_id: int
    symbol: str
    date: str
    reported_currency: str
    cik: str
    filing_date: str
    accepted_date: str
    fiscal_year: str
    period: str
    revenue: int
    cost_of_revenue: int
    gross_profit: int
    research_and_development_expenses: int
    general_and_administrative_expenses: int
    selling_and_marketing_expenses: int
    selling_general_and_administrative_expenses: int
    other_expenses: int
    operating_expenses: int
    cost_and_expenses: int
    net_interest_income: int
    interest_income: int
    interest_expense: int
    depreciation_and_amortization: int
    ebitda: int
    ebit: int
    non_operating_income_excluding_interest: int
    operating_income: int
    total_other_income_expenses_net: int
    income_before_tax: int
    income_tax_expense: int
    net_income_from_continuing_operations: int
    net_income_from_discontinued_operations: int
    other_adjustments_to_net_income: int
    net_income: int
    net_income_deductions: int
    bottom_line_net_income: int
    eps: float
    eps_diluted: float
    weighted_average_shs_out: int
    weighted_average_shs_out_dil: int


class CompanyIncomeStatementWrite(CompanyIncomeStatement):
    model_config = ConfigDict(from_attributes=True)


class CompanyIncomeStatementRead(CompanyIncomeStatement):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
