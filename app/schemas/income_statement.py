from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyIncomeStatement(BaseModel):
    company_id: int
    symbol: str
    date: date_type
    reported_currency: str
    cik: str
    filing_date: date_type
    accepted_date: datetime
    fiscal_year: int
    period: str
    revenue: Optional[int] = None
    cost_of_revenue: Optional[int] = None
    gross_profit: Optional[int] = None
    research_and_development_expenses: Optional[int] = None
    general_and_administrative_expenses: Optional[int] = None
    selling_and_marketing_expenses: Optional[int] = None
    selling_general_and_administrative_expenses: Optional[int] = None
    other_expenses: Optional[int] = None
    operating_expenses: Optional[int] = None
    cost_and_expenses: Optional[int] = None
    net_interest_income: Optional[int] = None
    interest_income: Optional[int] = None
    interest_expense: Optional[int] = None
    depreciation_and_amortization: Optional[int] = None
    ebitda: Optional[int] = None
    ebit: Optional[int] = None
    non_operating_income_excluding_interest: Optional[int] = None
    operating_income: Optional[int] = None
    total_other_income_expenses_net: Optional[int] = None
    income_before_tax: Optional[int] = None
    income_tax_expense: Optional[int] = None
    net_income_from_continuing_operations: Optional[int] = None
    net_income_from_discontinued_operations: Optional[int] = None
    other_adjustments_to_net_income: Optional[int] = None
    net_income: Optional[int] = None
    net_income_deductions: Optional[int] = None
    bottom_line_net_income: Optional[int] = None
    eps: Optional[float] = None
    eps_diluted: Optional[float] = None
    weighted_average_shs_out: Optional[int] = None
    weighted_average_shs_out_dil: Optional[int] = None


class CompanyIncomeStatementWrite(CompanyIncomeStatement):
    model_config = ConfigDict(from_attributes=True)


class CompanyIncomeStatementRead(CompanyIncomeStatement):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
