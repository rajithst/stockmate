from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyCashFlowStatement(Base):
    __tablename__ = "company_cash_flow_statements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), index=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    # General report info
    date: Mapped[str]
    reported_currency: Mapped[str]
    cik: Mapped[str]
    filing_date: Mapped[str]
    accepted_date: Mapped[str]
    fiscal_year: Mapped[str]
    period: Mapped[str]

    # Operating Activities
    net_income: Mapped[int]
    depreciation_and_amortization: Mapped[int]
    deferred_income_tax: Mapped[int]
    stock_based_compensation: Mapped[int]
    change_in_working_capital: Mapped[int]
    accounts_receivables: Mapped[int]
    inventory: Mapped[int]
    accounts_payables: Mapped[int]
    other_working_capital: Mapped[int]
    other_non_cash_items: Mapped[int]
    net_cash_provided_by_operating_activities: Mapped[int]

    # Investing Activities
    investments_in_property_plant_and_equipment: Mapped[int]
    acquisitions_net: Mapped[int]
    purchases_of_investments: Mapped[int]
    sales_maturities_of_investments: Mapped[int]
    other_investing_activities: Mapped[int]
    net_cash_provided_by_investing_activities: Mapped[int]

    # Financing Activities
    net_debt_issuance: Mapped[int]
    long_term_net_debt_issuance: Mapped[int]
    short_term_net_debt_issuance: Mapped[int]
    net_stock_issuance: Mapped[int]
    net_common_stock_issuance: Mapped[int]
    common_stock_issuance: Mapped[int]
    common_stock_repurchased: Mapped[int]
    net_preferred_stock_issuance: Mapped[int]
    net_dividends_paid: Mapped[int]
    common_dividends_paid: Mapped[int]
    preferred_dividends_paid: Mapped[int]
    other_financing_activities: Mapped[int]
    net_cash_provided_by_financing_activities: Mapped[int]

    # Other Adjustments
    effect_of_forex_changes_on_cash: Mapped[int]
    net_change_in_cash: Mapped[int]
    cash_at_end_of_period: Mapped[int]
    cash_at_beginning_of_period: Mapped[int]
    operating_cash_flow: Mapped[int]
    capital_expenditure: Mapped[int]
    free_cash_flow: Mapped[int]
    income_taxes_paid: Mapped[int]
    interest_paid: Mapped[int]

    # Relationship to company profile
    company: Mapped["Company"] = relationship(back_populates="cash_flow_statements")

    def __repr__(self):
        return f"<CompanyCashFlowStatement(symbol={self.symbol}, date={self.date})>"
