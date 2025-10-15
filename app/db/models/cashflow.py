from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.engine import Base


class CompanyCashFlowStatement(Base):
    __tablename__ = "company_cash_flow_statements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    # General report info
    date: Mapped[str] = mapped_column(String(20))
    reported_currency: Mapped[str] = mapped_column(String(10))
    cik: Mapped[str] = mapped_column(String(20))
    filing_date: Mapped[str] = mapped_column(String(20))
    accepted_date: Mapped[str] = mapped_column(String(20))
    fiscal_year: Mapped[str] = mapped_column(String(10))
    period: Mapped[str] = mapped_column(String(10))

    # Operating Activities
    net_income: Mapped[int] = mapped_column(Integer)
    depreciation_and_amortization: Mapped[int] = mapped_column(Integer)
    deferred_income_tax: Mapped[int] = mapped_column(Integer)
    stock_based_compensation: Mapped[int] = mapped_column(Integer)
    change_in_working_capital: Mapped[int] = mapped_column(Integer)
    accounts_receivables: Mapped[int] = mapped_column(Integer)
    inventory: Mapped[int] = mapped_column(Integer)
    accounts_payables: Mapped[int] = mapped_column(Integer)
    other_working_capital: Mapped[int] = mapped_column(Integer)
    other_non_cash_items: Mapped[int] = mapped_column(Integer)
    net_cash_provided_by_operating_activities: Mapped[int] = mapped_column(Integer)

    # Investing Activities
    investments_in_property_plant_and_equipment: Mapped[int] = mapped_column(Integer)
    acquisitions_net: Mapped[int] = mapped_column(Integer)
    purchases_of_investments: Mapped[int] = mapped_column(Integer)
    sales_maturities_of_investments: Mapped[int] = mapped_column(Integer)
    other_investing_activities: Mapped[int] = mapped_column(Integer)
    net_cash_provided_by_investing_activities: Mapped[int] = mapped_column(Integer)

    # Financing Activities
    net_debt_issuance: Mapped[int] = mapped_column(Integer)
    long_term_net_debt_issuance: Mapped[int] = mapped_column(Integer)
    short_term_net_debt_issuance: Mapped[int] = mapped_column(Integer)
    net_stock_issuance: Mapped[int] = mapped_column(Integer)
    net_common_stock_issuance: Mapped[int] = mapped_column(Integer)
    common_stock_issuance: Mapped[int] = mapped_column(Integer)
    common_stock_repurchased: Mapped[int] = mapped_column(Integer)
    net_preferred_stock_issuance: Mapped[int] = mapped_column(Integer)
    net_dividends_paid: Mapped[int] = mapped_column(Integer)
    common_dividends_paid: Mapped[int] = mapped_column(Integer)
    preferred_dividends_paid: Mapped[int] = mapped_column(Integer)
    other_financing_activities: Mapped[int] = mapped_column(Integer)
    net_cash_provided_by_financing_activities: Mapped[int] = mapped_column(Integer)

    # Other Adjustments
    effect_of_forex_changes_on_cash: Mapped[int] = mapped_column(Integer)
    net_change_in_cash: Mapped[int] = mapped_column(Integer)
    cash_at_end_of_period: Mapped[int] = mapped_column(Integer)
    cash_at_beginning_of_period: Mapped[int] = mapped_column(Integer)
    operating_cash_flow: Mapped[int] = mapped_column(Integer)
    capital_expenditure: Mapped[int] = mapped_column(Integer)
    free_cash_flow: Mapped[int] = mapped_column(Integer)
    income_taxes_paid: Mapped[int] = mapped_column(Integer)
    interest_paid: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationship to company profile
    company: Mapped["Company"] = relationship(back_populates="cash_flow_statements")

    def __repr__(self):
        return f"<CompanyCashFlowStatement(symbol={self.symbol}, date={self.date})>"
