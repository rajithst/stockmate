from sqlalchemy import String, Integer, Float, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.engine import Base


class CompanyKeyMetrics(Base):
    __tablename__ = "company_key_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), index=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=False)
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=False)
    period: Mapped[str] = mapped_column(String(10), nullable=False)
    reported_currency: Mapped[str] = mapped_column(String(10), nullable=False)

    # Market metrics
    market_cap: Mapped[int] = mapped_column(nullable=True)
    enterprise_value: Mapped[int] = mapped_column(nullable=True)
    ev_to_sales: Mapped[float] = mapped_column(nullable=True)
    ev_to_operating_cash_flow: Mapped[float] = mapped_column(nullable=True)
    ev_to_free_cash_flow: Mapped[float] = mapped_column(nullable=True)
    ev_to_ebitda: Mapped[float] = mapped_column(nullable=True)
    net_debt_to_ebitda: Mapped[float] = mapped_column(nullable=True)
    current_ratio: Mapped[float] = mapped_column(nullable=True)
    income_quality: Mapped[float] = mapped_column(nullable=True)
    graham_number: Mapped[float] = mapped_column(nullable=True)
    graham_net_net: Mapped[float] = mapped_column(nullable=True)
    tax_burden: Mapped[float] = mapped_column(nullable=True)
    interest_burden: Mapped[float] = mapped_column(nullable=True)

    # Capital metrics
    working_capital: Mapped[int] = mapped_column(nullable=True)
    invested_capital: Mapped[int] = mapped_column(nullable=True)
    return_on_assets: Mapped[float] = mapped_column(nullable=True)
    operating_return_on_assets: Mapped[float] = mapped_column(nullable=True)
    return_on_tangible_assets: Mapped[float] = mapped_column(nullable=True)
    return_on_equity: Mapped[float] = mapped_column(nullable=True)
    return_on_invested_capital: Mapped[float] = mapped_column(nullable=True)
    return_on_capital_employed: Mapped[float] = mapped_column(nullable=True)

    # Cash flow metrics
    earnings_yield: Mapped[float] = mapped_column(nullable=True)
    free_cash_flow_yield: Mapped[float] = mapped_column(nullable=True)
    capex_to_operating_cash_flow: Mapped[float] = mapped_column(nullable=True)
    capex_to_depreciation: Mapped[float] = mapped_column(nullable=True)
    capex_to_revenue: Mapped[float] = mapped_column(nullable=True)

    # Operational efficiency
    sales_general_and_administrative_to_revenue: Mapped[float] = mapped_column(nullable=True)
    research_and_development_to_revenue: Mapped[float] = mapped_column(nullable=True)
    stock_based_compensation_to_revenue: Mapped[float] = mapped_column(nullable=True)
    intangibles_to_total_assets: Mapped[float] = mapped_column(nullable=True)
    average_receivables: Mapped[int] = mapped_column(nullable=True)
    average_payables: Mapped[int] = mapped_column(nullable=True)
    average_inventory: Mapped[int] = mapped_column(nullable=True)
    days_of_sales_outstanding: Mapped[float] = mapped_column(nullable=True)
    days_of_payables_outstanding: Mapped[float] = mapped_column(nullable=True)
    days_of_inventory_outstanding: Mapped[float] = mapped_column(nullable=True)
    operating_cycle: Mapped[float] = mapped_column(nullable=True)
    cash_conversion_cycle: Mapped[float] = mapped_column(nullable=True)
    free_cash_flow_to_equity: Mapped[float] = mapped_column(nullable=True)
    free_cash_flow_to_firm: Mapped[float] = mapped_column(nullable=True)
    tangible_asset_value: Mapped[int] = mapped_column(nullable=True)
    net_current_asset_value: Mapped[int] = mapped_column(nullable=True)

    # Relationship to company
    company: Mapped["Company"] = relationship(back_populates="key_metrics")

    def __repr__(self):
        return f"<CompanyKeyMetrics(symbol={self.symbol}, date={self.date})>"
