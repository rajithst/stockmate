from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyBalanceSheet(Base):
    __tablename__ = "company_balance_sheets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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

    # Current Assets
    cash_and_cash_equivalents: Mapped[int]
    short_term_investments: Mapped[int]
    cash_and_short_term_investments: Mapped[int]
    net_receivables: Mapped[int]
    accounts_receivables: Mapped[int]
    other_receivables: Mapped[int]
    inventory: Mapped[int]
    prepaids: Mapped[int]
    other_current_assets: Mapped[int]
    total_current_assets: Mapped[int]

    # Non-Current Assets
    property_plant_equipment_net: Mapped[int]
    goodwill: Mapped[int]
    intangible_assets: Mapped[int]
    goodwill_and_intangible_assets: Mapped[int]
    long_term_investments: Mapped[int]
    tax_assets: Mapped[int]
    other_non_current_assets: Mapped[int]
    total_non_current_assets: Mapped[int]
    other_assets: Mapped[int]
    total_assets: Mapped[int]

    # Current Liabilities
    total_payables: Mapped[int]
    account_payables: Mapped[int]
    other_payables: Mapped[int]
    accrued_expenses: Mapped[int]
    short_term_debt: Mapped[int]
    capital_lease_obligations_current: Mapped[int]
    tax_payables: Mapped[int]
    deferred_revenue: Mapped[int]
    other_current_liabilities: Mapped[int]
    total_current_liabilities: Mapped[int]

    # Non-Current Liabilities
    long_term_debt: Mapped[int]
    deferred_revenue_non_current: Mapped[int]
    deferred_tax_liabilities_non_current: Mapped[int]
    other_non_current_liabilities: Mapped[int]
    total_non_current_liabilities: Mapped[int]
    other_liabilities: Mapped[int]
    capital_lease_obligations: Mapped[int]
    total_liabilities: Mapped[int]

    # Stockholders' Equity
    treasury_stock: Mapped[int]
    preferred_stock: Mapped[int]
    common_stock: Mapped[int]
    retained_earnings: Mapped[int]
    additional_paid_in_capital: Mapped[int]
    accumulated_other_comprehensive_income_loss: Mapped[int]
    other_total_stockholders_equity: Mapped[int]
    total_stockholders_equity: Mapped[int]
    total_equity: Mapped[int]
    minority_interest: Mapped[int]

    # Totals & Debt
    total_liabilities_and_total_equity: Mapped[int]
    total_investments: Mapped[int]
    total_debt: Mapped[int]
    net_debt: Mapped[int]

    # Relationship to company profile
    company: Mapped["Company"] = relationship(back_populates="balance_sheets")

    def __repr__(self):
        return f"<CompanyBalanceSheet(symbol={self.symbol}, date={self.date})>"
