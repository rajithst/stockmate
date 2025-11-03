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


class CompanyCashFlowStatement(Base):
    __tablename__ = "company_cash_flow_statements"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "fiscal_year", "period", name="uq_cashflow_period"
        ),
        Index("ix_cashflow_symbol_date", "symbol", "date"),
        Index("ix_cashflow_fiscal_year", "fiscal_year"),
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
    period: Mapped[str] = mapped_column(String(10))

    # Operating Activities
    net_income: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    depreciation_and_amortization: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    deferred_income_tax: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    stock_based_compensation: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    change_in_working_capital: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    accounts_receivables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    inventory: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    accounts_payables: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    other_working_capital: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    other_non_cash_items: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    net_cash_provided_by_operating_activities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )

    # Investing Activities
    investments_in_property_plant_and_equipment: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    acquisitions_net: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    purchases_of_investments: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    sales_maturities_of_investments: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_investing_activities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_cash_provided_by_investing_activities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )

    # Financing Activities
    net_debt_issuance: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    long_term_net_debt_issuance: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    short_term_net_debt_issuance: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_stock_issuance: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    net_common_stock_issuance: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    common_stock_issuance: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    common_stock_repurchased: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_preferred_stock_issuance: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_dividends_paid: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    common_dividends_paid: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    preferred_dividends_paid: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    other_financing_activities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_cash_provided_by_financing_activities: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )

    # Other Adjustments
    effect_of_forex_changes_on_cash: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    net_change_in_cash: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    cash_at_end_of_period: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    cash_at_beginning_of_period: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    operating_cash_flow: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    capital_expenditure: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    free_cash_flow: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    income_taxes_paid: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    interest_paid: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
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
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyCashFlowStatement(symbol={self.symbol}, date={self.date})>"
