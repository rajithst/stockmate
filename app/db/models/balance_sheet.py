from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyBalanceSheet(Base):
    __tablename__ = "company_balance_sheets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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

    # Current Assets
    cash_and_cash_equivalents: Mapped[int] = mapped_column(BigInteger)
    short_term_investments: Mapped[int] = mapped_column(BigInteger)
    cash_and_short_term_investments: Mapped[int] = mapped_column(BigInteger)
    net_receivables: Mapped[int] = mapped_column(BigInteger)
    accounts_receivables: Mapped[int] = mapped_column(BigInteger)
    other_receivables: Mapped[int] = mapped_column(BigInteger)
    inventory: Mapped[int] = mapped_column(BigInteger)
    prepaids: Mapped[int] = mapped_column(BigInteger)
    other_current_assets: Mapped[int] = mapped_column(BigInteger)
    total_current_assets: Mapped[int] = mapped_column(BigInteger)

    # Non-Current Assets
    property_plant_equipment_net: Mapped[int] = mapped_column(BigInteger)
    goodwill: Mapped[int] = mapped_column(BigInteger)
    intangible_assets: Mapped[int] = mapped_column(BigInteger)
    goodwill_and_intangible_assets: Mapped[int] = mapped_column(BigInteger)
    long_term_investments: Mapped[int] = mapped_column(BigInteger)
    tax_assets: Mapped[int] = mapped_column(BigInteger)
    other_non_current_assets: Mapped[int] = mapped_column(BigInteger)
    total_non_current_assets: Mapped[int] = mapped_column(BigInteger)
    other_assets: Mapped[int] = mapped_column(BigInteger)
    total_assets: Mapped[int] = mapped_column(BigInteger)

    # Current Liabilities
    total_payables: Mapped[int] = mapped_column(BigInteger)
    account_payables: Mapped[int] = mapped_column(BigInteger)
    other_payables: Mapped[int] = mapped_column(BigInteger)
    accrued_expenses: Mapped[int] = mapped_column(BigInteger)
    short_term_debt: Mapped[int] = mapped_column(BigInteger)
    capital_lease_obligations_current: Mapped[int] = mapped_column(BigInteger)
    tax_payables: Mapped[int] = mapped_column(BigInteger)
    deferred_revenue: Mapped[int] = mapped_column(BigInteger)
    other_current_liabilities: Mapped[int] = mapped_column(BigInteger)
    total_current_liabilities: Mapped[int] = mapped_column(BigInteger)

    # Non-Current Liabilities
    long_term_debt: Mapped[int] = mapped_column(BigInteger)
    deferred_revenue_non_current: Mapped[int] = mapped_column(BigInteger)
    deferred_tax_liabilities_non_current: Mapped[int] = mapped_column(BigInteger)
    other_non_current_liabilities: Mapped[int] = mapped_column(BigInteger)
    total_non_current_liabilities: Mapped[int] = mapped_column(BigInteger)
    other_liabilities: Mapped[int] = mapped_column(BigInteger)
    capital_lease_obligations: Mapped[int] = mapped_column(BigInteger)
    total_liabilities: Mapped[int] = mapped_column(BigInteger)

    # Stockholders' Equity
    treasury_stock: Mapped[int] = mapped_column(BigInteger)
    preferred_stock: Mapped[int] = mapped_column(BigInteger)
    common_stock: Mapped[int] = mapped_column(BigInteger)
    retained_earnings: Mapped[int] = mapped_column(BigInteger)
    additional_paid_in_capital: Mapped[int] = mapped_column(BigInteger)
    accumulated_other_comprehensive_income_loss: Mapped[int] = mapped_column(BigInteger)
    other_total_stockholders_equity: Mapped[int] = mapped_column(BigInteger)
    total_stockholders_equity: Mapped[int] = mapped_column(BigInteger)
    total_equity: Mapped[int] = mapped_column(BigInteger)
    minority_interest: Mapped[int] = mapped_column(BigInteger)

    # Totals & Debt
    total_liabilities_and_total_equity: Mapped[int] = mapped_column(BigInteger)
    total_investments: Mapped[int] = mapped_column(BigInteger)
    total_debt: Mapped[int] = mapped_column(BigInteger)
    net_debt: Mapped[int] = mapped_column(BigInteger)
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
        lazy="joined",
    )

    def __repr__(self):
        return f"<CompanyBalanceSheet(symbol={self.symbol}, date={self.date})>"
