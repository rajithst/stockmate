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


class CompanyBalanceSheet(Base):
    __tablename__ = "company_balance_sheets"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "fiscal_year", "period", name="uq_balance_sheet_period"
        ),
        Index("ix_balance_sheet_symbol_date", "symbol", "date"),
        Index("ix_balance_sheet_fiscal_year", "fiscal_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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

    # Current Assets
    cash_and_cash_equivalents: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    short_term_investments: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    cash_and_short_term_investments: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_receivables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    accounts_receivables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    other_receivables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    inventory: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    prepaids: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    other_current_assets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    total_current_assets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Non-Current Assets
    property_plant_equipment_net: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    goodwill: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    intangible_assets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    goodwill_and_intangible_assets: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    long_term_investments: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tax_assets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    other_non_current_assets: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    total_non_current_assets: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_assets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    total_assets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Current Liabilities
    total_payables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    account_payables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    other_payables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    accrued_expenses: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    short_term_debt: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    capital_lease_obligations_current: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    tax_payables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    deferred_revenue: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    other_current_liabilities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    total_current_liabilities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )

    # Non-Current Liabilities
    long_term_debt: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    deferred_revenue_non_current: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    deferred_tax_liabilities_non_current: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_non_current_liabilities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    total_non_current_liabilities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_liabilities: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    capital_lease_obligations: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    total_liabilities: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Stockholders' Equity
    treasury_stock: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    preferred_stock: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    common_stock: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    retained_earnings: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    additional_paid_in_capital: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    accumulated_other_comprehensive_income_loss: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_total_stockholders_equity: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    total_stockholders_equity: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    total_equity: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    minority_interest: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Totals & Debt
    total_liabilities_and_total_equity: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    total_investments: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    total_debt: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    net_debt: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
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
        back_populates="balance_sheets",
        foreign_keys=[company_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyBalanceSheet(symbol={self.symbol}, date={self.date})>"
