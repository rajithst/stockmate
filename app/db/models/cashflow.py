from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyCashFlowStatement(Base):
    __tablename__ = "company_cash_flow_statements"

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
    accepted_date: Mapped[str] = mapped_column(String(20))
    fiscal_year: Mapped[str] = mapped_column(String(10))
    period: Mapped[str] = mapped_column(String(10))

    # Operating Activities
    net_income: Mapped[int] = mapped_column(BigInteger)
    depreciation_and_amortization: Mapped[int] = mapped_column(BigInteger)
    deferred_income_tax: Mapped[int] = mapped_column(BigInteger)
    stock_based_compensation: Mapped[int] = mapped_column(BigInteger)
    change_in_working_capital: Mapped[int] = mapped_column(BigInteger)
    accounts_receivables: Mapped[int] = mapped_column(BigInteger)
    inventory: Mapped[int] = mapped_column(BigInteger)
    accounts_payables: Mapped[int] = mapped_column(BigInteger)
    other_working_capital: Mapped[int] = mapped_column(BigInteger)
    other_non_cash_items: Mapped[int] = mapped_column(BigInteger)
    net_cash_provided_by_operating_activities: Mapped[int] = mapped_column(BigInteger)

    # Investing Activities
    investments_in_property_plant_and_equipment: Mapped[int] = mapped_column(BigInteger)
    acquisitions_net: Mapped[int] = mapped_column(BigInteger)
    purchases_of_investments: Mapped[int] = mapped_column(BigInteger)
    sales_maturities_of_investments: Mapped[int] = mapped_column(BigInteger)
    other_investing_activities: Mapped[int] = mapped_column(BigInteger)
    net_cash_provided_by_investing_activities: Mapped[int] = mapped_column(BigInteger)

    # Financing Activities
    net_debt_issuance: Mapped[int] = mapped_column(BigInteger)
    long_term_net_debt_issuance: Mapped[int] = mapped_column(BigInteger)
    short_term_net_debt_issuance: Mapped[int] = mapped_column(BigInteger)
    net_stock_issuance: Mapped[int] = mapped_column(BigInteger)
    net_common_stock_issuance: Mapped[int] = mapped_column(BigInteger)
    common_stock_issuance: Mapped[int] = mapped_column(BigInteger)
    common_stock_repurchased: Mapped[int] = mapped_column(BigInteger)
    net_preferred_stock_issuance: Mapped[int] = mapped_column(BigInteger)
    net_dividends_paid: Mapped[int] = mapped_column(BigInteger)
    common_dividends_paid: Mapped[int] = mapped_column(BigInteger)
    preferred_dividends_paid: Mapped[int] = mapped_column(BigInteger)
    other_financing_activities: Mapped[int] = mapped_column(BigInteger)
    net_cash_provided_by_financing_activities: Mapped[int] = mapped_column(BigInteger)

    # Other Adjustments
    effect_of_forex_changes_on_cash: Mapped[int] = mapped_column(BigInteger)
    net_change_in_cash: Mapped[int] = mapped_column(BigInteger)
    cash_at_end_of_period: Mapped[int] = mapped_column(BigInteger)
    cash_at_beginning_of_period: Mapped[int] = mapped_column(BigInteger)
    operating_cash_flow: Mapped[int] = mapped_column(BigInteger)
    capital_expenditure: Mapped[int] = mapped_column(BigInteger)
    free_cash_flow: Mapped[int] = mapped_column(BigInteger)
    income_taxes_paid: Mapped[int] = mapped_column(BigInteger)
    interest_paid: Mapped[int] = mapped_column(BigInteger)
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
        back_populates="cash_flow_statements",
        foreign_keys=[company_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<CompanyCashFlowStatement(symbol={self.symbol}, date={self.date})>"
