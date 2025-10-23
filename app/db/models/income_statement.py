from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyIncomeStatement(Base):
    __tablename__ = "company_income_statements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
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
    revenue: Mapped[int] = mapped_column(BigInteger)
    cost_of_revenue: Mapped[int] = mapped_column(BigInteger)
    gross_profit: Mapped[int] = mapped_column(BigInteger)

    # Operating expenses
    research_and_development_expenses: Mapped[int] = mapped_column(BigInteger)
    general_and_administrative_expenses: Mapped[int] = mapped_column(BigInteger)
    selling_and_marketing_expenses: Mapped[int] = mapped_column(BigInteger)
    selling_general_and_administrative_expenses: Mapped[int] = mapped_column(BigInteger)
    other_expenses: Mapped[int] = mapped_column(BigInteger)
    operating_expenses: Mapped[int] = mapped_column(BigInteger)
    cost_and_expenses: Mapped[int] = mapped_column(BigInteger)

    # Interest income/expense
    net_interest_income: Mapped[int] = mapped_column(BigInteger)
    interest_income: Mapped[int] = mapped_column(BigInteger)
    interest_expense: Mapped[int] = mapped_column(BigInteger)

    # Depreciation & amortization
    depreciation_and_amortization: Mapped[int] = mapped_column(BigInteger)

    # Profit metrics
    ebitda: Mapped[int] = mapped_column(BigInteger)
    ebit: Mapped[int] = mapped_column(BigInteger)
    non_operating_income_excluding_interest: Mapped[int] = mapped_column(BigInteger)
    operating_income: Mapped[int] = mapped_column(BigInteger)

    # Other income/expenses & taxes
    total_other_income_expenses_net: Mapped[int] = mapped_column(BigInteger)
    income_before_tax: Mapped[int] = mapped_column(BigInteger)
    income_tax_expense: Mapped[int] = mapped_column(BigInteger)

    # Net income details
    net_income_from_continuing_operations: Mapped[int] = mapped_column(BigInteger)
    net_income_from_discontinued_operations: Mapped[int] = mapped_column(BigInteger)
    other_adjustments_to_net_income: Mapped[int] = mapped_column(BigInteger)
    net_income: Mapped[int] = mapped_column(BigInteger)
    net_income_deductions: Mapped[int] = mapped_column(BigInteger)
    bottom_line_net_income: Mapped[int] = mapped_column(BigInteger)

    # Earnings per share
    eps: Mapped[float] = mapped_column(Float)
    eps_diluted: Mapped[float] = mapped_column(Float)
    weighted_average_shs_out: Mapped[int] = mapped_column(BigInteger)
    weighted_average_shs_out_dil: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship to company profile
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="income_statements",
        foreign_keys=[company_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<CompanyIncomeStatement(symbol={self.symbol}, date={self.date})>"
