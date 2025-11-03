from datetime import date as date_type, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyIncomeStatement(Base):
    __tablename__ = "company_income_statements"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "fiscal_year", "period", name="uq_income_period"
        ),
        Index("ix_income_symbol_date", "symbol", "date"),
        Index("ix_income_fiscal_year", "fiscal_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    # General report info
    date: Mapped[date_type] = mapped_column(Date)
    reported_currency: Mapped[str] = mapped_column(String(10))
    cik: Mapped[str] = mapped_column(String(20))
    filing_date: Mapped[date_type] = mapped_column(Date)
    accepted_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    fiscal_year: Mapped[int] = mapped_column(index=True)
    period: Mapped[str] = mapped_column(String(5))

    # Revenue and cost
    revenue: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    cost_of_revenue: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    gross_profit: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Operating expenses
    research_and_development_expenses: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    general_and_administrative_expenses: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    selling_and_marketing_expenses: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    selling_general_and_administrative_expenses: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_expenses: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    operating_expenses: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    cost_and_expenses: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Interest income/expense
    net_interest_income: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    interest_income: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    interest_expense: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Depreciation & amortization
    depreciation_and_amortization: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )

    # Profit metrics
    ebitda: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    ebit: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    non_operating_income_excluding_interest: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    operating_income: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Other income/expenses & taxes
    total_other_income_expenses_net: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    income_before_tax: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    income_tax_expense: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Net income details
    net_income_from_continuing_operations: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_income_from_discontinued_operations: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_adjustments_to_net_income: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_income: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    net_income_deductions: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    bottom_line_net_income: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )

    # Earnings per share
    eps: Mapped[float | None] = mapped_column(nullable=True)
    eps_diluted: Mapped[float | None] = mapped_column(nullable=True)
    weighted_average_shs_out: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    weighted_average_shs_out_dil: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
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
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyIncomeStatement(symbol={self.symbol}, date={self.date})>"
