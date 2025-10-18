from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
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
    cash_and_cash_equivalents: Mapped[int] = mapped_column(Integer)
    short_term_investments: Mapped[int] = mapped_column(Integer)
    cash_and_short_term_investments: Mapped[int] = mapped_column(Integer)
    net_receivables: Mapped[int] = mapped_column(Integer)
    accounts_receivables: Mapped[int] = mapped_column(Integer)
    other_receivables: Mapped[int] = mapped_column(Integer)
    inventory: Mapped[int] = mapped_column(Integer)
    prepaids: Mapped[int] = mapped_column(Integer)
    other_current_assets: Mapped[int] = mapped_column(Integer)
    total_current_assets: Mapped[int] = mapped_column(Integer)

    # Non-Current Assets
    property_plant_equipment_net: Mapped[int] = mapped_column(Integer)
    goodwill: Mapped[int] = mapped_column(Integer)
    intangible_assets: Mapped[int] = mapped_column(Integer)
    goodwill_and_intangible_assets: Mapped[int] = mapped_column(Integer)
    long_term_investments: Mapped[int] = mapped_column(Integer)
    tax_assets: Mapped[int] = mapped_column(Integer)
    other_non_current_assets: Mapped[int] = mapped_column(Integer)
    total_non_current_assets: Mapped[int] = mapped_column(Integer)
    other_assets: Mapped[int] = mapped_column(Integer)
    total_assets: Mapped[int] = mapped_column(Integer)

    # Current Liabilities
    total_payables: Mapped[int] = mapped_column(Integer)
    account_payables: Mapped[int] = mapped_column(Integer)
    other_payables: Mapped[int] = mapped_column(Integer)
    accrued_expenses: Mapped[int] = mapped_column(Integer)
    short_term_debt: Mapped[int] = mapped_column(Integer)
    capital_lease_obligations_current: Mapped[int] = mapped_column(Integer)
    tax_payables: Mapped[int] = mapped_column(Integer)
    deferred_revenue: Mapped[int] = mapped_column(Integer)
    other_current_liabilities: Mapped[int] = mapped_column(Integer)
    total_current_liabilities: Mapped[int] = mapped_column(Integer)

    # Non-Current Liabilities
    long_term_debt: Mapped[int] = mapped_column(Integer)
    deferred_revenue_non_current: Mapped[int] = mapped_column(Integer)
    deferred_tax_liabilities_non_current: Mapped[int] = mapped_column(Integer)
    other_non_current_liabilities: Mapped[int] = mapped_column(Integer)
    total_non_current_liabilities: Mapped[int] = mapped_column(Integer)
    other_liabilities: Mapped[int] = mapped_column(Integer)
    capital_lease_obligations: Mapped[int] = mapped_column(Integer)
    total_liabilities: Mapped[int] = mapped_column(Integer)

    # Stockholders' Equity
    treasury_stock: Mapped[int] = mapped_column(Integer)
    preferred_stock: Mapped[int] = mapped_column(Integer)
    common_stock: Mapped[int] = mapped_column(Integer)
    retained_earnings: Mapped[int] = mapped_column(Integer)
    additional_paid_in_capital: Mapped[int] = mapped_column(Integer)
    accumulated_other_comprehensive_income_loss: Mapped[int] = mapped_column(Integer)
    other_total_stockholders_equity: Mapped[int] = mapped_column(Integer)
    total_stockholders_equity: Mapped[int] = mapped_column(Integer)
    total_equity: Mapped[int] = mapped_column(Integer)
    minority_interest: Mapped[int] = mapped_column(Integer)

    # Totals & Debt
    total_liabilities_and_total_equity: Mapped[int] = mapped_column(Integer)
    total_investments: Mapped[int] = mapped_column(Integer)
    total_debt: Mapped[int] = mapped_column(Integer)
    net_debt: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationship to company profile
    company: Mapped["Company"] = relationship(back_populates="balance_sheets")

    def __repr__(self):
        return f"<CompanyBalanceSheet(symbol={self.symbol}, date={self.date})>"
