from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyIncomeStatement(Base):
    __tablename__ = "company_income_statements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), index=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    # General report info
    date: Mapped[str] = mapped_column(String(20))
    reported_currency: Mapped[str] = mapped_column(String(10))
    cik: Mapped[str] = mapped_column(String(20))
    filing_date: Mapped[str] = mapped_column(String(20))
    accepted_date: Mapped[str] = mapped_column(String(30))
    fiscal_year: Mapped[str] = mapped_column(String(10))
    period: Mapped[str] = mapped_column(String(5))

    # Revenue and cost
    revenue: Mapped[int]
    cost_of_revenue: Mapped[int]
    gross_profit: Mapped[int]

    # Operating expenses
    research_and_development_expenses: Mapped[int]
    general_and_administrative_expenses: Mapped[int]
    selling_and_marketing_expenses: Mapped[int]
    selling_general_and_administrative_expenses: Mapped[int]
    other_expenses: Mapped[int]
    operating_expenses: Mapped[int]
    cost_and_expenses: Mapped[int]

    # Interest income/expense
    net_interest_income: Mapped[int]
    interest_income: Mapped[int]
    interest_expense: Mapped[int]

    # Depreciation & amortization
    depreciation_and_amortization: Mapped[int]

    # Profit metrics
    ebitda: Mapped[int]
    ebit: Mapped[int]
    non_operating_income_excluding_interest: Mapped[int]
    operating_income: Mapped[int]

    # Other income/expenses & taxes
    total_other_income_expenses_net: Mapped[int]
    income_before_tax: Mapped[int]
    income_tax_expense: Mapped[int]

    # Net income details
    net_income_from_continuing_operations: Mapped[int]
    net_income_from_discontinued_operations: Mapped[int]
    other_adjustments_to_net_income: Mapped[int]
    net_income: Mapped[int]
    net_income_deductions: Mapped[int]
    bottom_line_net_income: Mapped[int]

    # Earnings per share
    eps: Mapped[float]
    eps_diluted: Mapped[float]
    weighted_average_shs_out: Mapped[int]
    weighted_average_shs_out_dil: Mapped[int]

    # Relationship to company profile
    company: Mapped["Company"] = relationship(back_populates="income_statements")

    def __repr__(self):
        return f"<CompanyIncomeStatement(symbol={self.symbol}, date={self.date})>"
