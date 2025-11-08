"""
Company Metrics Models

Contains all company metrics and valuation related models:
- CompanyAnalystEstimate: Analyst forecasts for revenue, earnings, etc.
- CompanyKeyMetrics: Key performance and valuation metrics
- DiscountedCashFlow: DCF valuation model data
- CompanyRevenueProductSegmentation: Revenue breakdown by product/segment
"""

from datetime import date as date_type, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyAnalystEstimate(Base):
    """Analyst estimates and forecasts for company financial metrics"""

    __tablename__ = "company_analyst_estimates"
    __table_args__ = (
        UniqueConstraint("symbol", "date", name="uq_analyst_estimate_date"),
        Index("ix_estimate_symbol_date", "symbol", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True, nullable=False)

    date: Mapped[date_type] = mapped_column(Date, nullable=False)

    # Revenue estimates (in millions)
    revenue_low: Mapped[float | None] = mapped_column(nullable=True)
    revenue_high: Mapped[float | None] = mapped_column(nullable=True)
    revenue_avg: Mapped[float | None] = mapped_column(nullable=True)

    # EBITDA estimates (in millions)
    ebitda_low: Mapped[float | None] = mapped_column(nullable=True)
    ebitda_high: Mapped[float | None] = mapped_column(nullable=True)
    ebitda_avg: Mapped[float | None] = mapped_column(nullable=True)

    # EBIT estimates (in millions)
    ebit_low: Mapped[float | None] = mapped_column(nullable=True)
    ebit_high: Mapped[float | None] = mapped_column(nullable=True)
    ebit_avg: Mapped[float | None] = mapped_column(nullable=True)

    # Net income estimates (in millions)
    net_income_low: Mapped[float | None] = mapped_column(nullable=True)
    net_income_high: Mapped[float | None] = mapped_column(nullable=True)
    net_income_avg: Mapped[float | None] = mapped_column(nullable=True)

    # SGA expense estimates (in millions)
    sga_expense_low: Mapped[float | None] = mapped_column(nullable=True)
    sga_expense_high: Mapped[float | None] = mapped_column(nullable=True)
    sga_expense_avg: Mapped[float | None] = mapped_column(nullable=True)

    # EPS estimates
    eps_avg: Mapped[float | None] = mapped_column(nullable=True)
    eps_high: Mapped[float | None] = mapped_column(nullable=True)
    eps_low: Mapped[float | None] = mapped_column(nullable=True)

    # Number of analysts
    num_analysts_revenue: Mapped[int | None] = mapped_column(nullable=True)
    num_analysts_eps: Mapped[int | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="analyst_estimates",
        foreign_keys=[company_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyAnalystEstimate(symbol={self.symbol}, date={self.date}, eps_avg={self.eps_avg})>"


class CompanyKeyMetrics(Base):
    """Key financial and valuation metrics for a company"""

    __tablename__ = "company_key_metrics"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "fiscal_year", "period", name="uq_metrics_period"
        ),
        Index("ix_metrics_symbol_date", "symbol", "date"),
        Index("ix_metrics_fiscal_year", "fiscal_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    fiscal_year: Mapped[int] = mapped_column(index=True, nullable=False)
    period: Mapped[str] = mapped_column(String(10), nullable=False)
    reported_currency: Mapped[str] = mapped_column(String(10), nullable=False)

    # Market metrics
    market_cap: Mapped[float | None] = mapped_column(Float, nullable=True)
    enterprise_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    ev_to_sales: Mapped[float | None] = mapped_column(nullable=True)
    ev_to_operating_cash_flow: Mapped[float | None] = mapped_column(nullable=True)
    ev_to_free_cash_flow: Mapped[float | None] = mapped_column(nullable=True)
    ev_to_ebitda: Mapped[float | None] = mapped_column(nullable=True)
    net_debt_to_ebitda: Mapped[float | None] = mapped_column(nullable=True)
    current_ratio: Mapped[float | None] = mapped_column(nullable=True)
    income_quality: Mapped[float | None] = mapped_column(nullable=True)
    graham_number: Mapped[float | None] = mapped_column(nullable=True)
    graham_net_net: Mapped[float | None] = mapped_column(nullable=True)
    tax_burden: Mapped[float | None] = mapped_column(nullable=True)
    interest_burden: Mapped[float | None] = mapped_column(nullable=True)

    # Capital metrics
    working_capital: Mapped[float | None] = mapped_column(Float, nullable=True)
    invested_capital: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_on_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    operating_return_on_assets: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    return_on_tangible_assets: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    return_on_equity: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_on_invested_capital: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    return_on_capital_employed: Mapped[float | None] = mapped_column(nullable=True)

    # Cash flow metrics
    earnings_yield: Mapped[float | None] = mapped_column(nullable=True)
    free_cash_flow_yield: Mapped[float | None] = mapped_column(nullable=True)
    capex_to_operating_cash_flow: Mapped[float | None] = mapped_column(nullable=True)
    capex_to_depreciation: Mapped[float | None] = mapped_column(nullable=True)
    capex_to_revenue: Mapped[float | None] = mapped_column(nullable=True)

    # Operational efficiency
    sales_general_and_administrative_to_revenue: Mapped[float | None] = mapped_column(
        nullable=True
    )
    research_and_development_to_revenue: Mapped[float | None] = mapped_column(
        nullable=True
    )
    stock_based_compensation_to_revenue: Mapped[float | None] = mapped_column(
        nullable=True
    )
    intangibles_to_total_assets: Mapped[float | None] = mapped_column(nullable=True)
    average_receivables: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_payables: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_inventory: Mapped[float | None] = mapped_column(Float, nullable=True)
    days_of_sales_outstanding: Mapped[float | None] = mapped_column(nullable=True)
    days_of_payables_outstanding: Mapped[float | None] = mapped_column(nullable=True)
    days_of_inventory_outstanding: Mapped[float | None] = mapped_column(nullable=True)
    operating_cycle: Mapped[float | None] = mapped_column(nullable=True)
    cash_conversion_cycle: Mapped[float | None] = mapped_column(nullable=True)
    free_cash_flow_to_equity: Mapped[float | None] = mapped_column(nullable=True)
    free_cash_flow_to_firm: Mapped[float | None] = mapped_column(nullable=True)
    tangible_asset_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_current_asset_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship to company
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="key_metrics",
        foreign_keys=[company_id],
        lazy="select",
    )

    def to_dict(self):
        return {
            "market_cap": self.market_cap,
            "enterprise_value": self.enterprise_value,
            "ev_to_sales": self.ev_to_sales,
            "ev_to_operating_cash_flow": self.ev_to_operating_cash_flow,
            "ev_to_free_cash_flow": self.ev_to_free_cash_flow,
            "ev_to_ebitda": self.ev_to_ebitda,
            "net_debt_to_ebitda": self.net_debt_to_ebitda,
            "current_ratio": self.current_ratio,
            "income_quality": self.income_quality,
            "graham_number": self.graham_number,
            "graham_net_net": self.graham_net_net,
            "tax_burden": self.tax_burden,
            "interest_burden": self.interest_burden,
            "working_capital": self.working_capital,
            "invested_capital": self.invested_capital,
            "return_on_assets": self.return_on_assets,
            "operating_return_on_assets": self.operating_return_on_assets,
            "return_on_tangible_assets": self.return_on_tangible_assets,
            "return_on_equity": self.return_on_equity,
            "return_on_invested_capital": self.return_on_invested_capital,
            "return_on_capital_employed": self.return_on_capital_employed,
            "earnings_yield": self.earnings_yield,
            "free_cash_flow_yield": self.free_cash_flow_yield,
            "capex_to_operating_cash_flow": self.capex_to_operating_cash_flow,
            "capex_to_depreciation": self.capex_to_depreciation,
            "capex_to_revenue": self.capex_to_revenue,
            "sales_general_and_administrative_to_revenue": self.sales_general_and_administrative_to_revenue,
            "research_and_development_to_revenue": self.research_and_development_to_revenue,
            "stock_based_compensation_to_revenue": self.stock_based_compensation_to_revenue,
            "intangibles_to_total_assets": self.intangibles_to_total_assets,
            "average_receivables": self.average_receivables,
            "average_payables": self.average_payables,
            "average_inventory": self.average_inventory,
            "days_of_sales_outstanding": self.days_of_sales_outstanding,
            "days_of_payables_outstanding": self.days_of_payables_outstanding,
            "days_of_inventory_outstanding": self.days_of_inventory_outstanding,
            "operating_cycle": self.operating_cycle,
            "cash_conversion_cycle": self.cash_conversion_cycle,
            "free_cash_flow_to_equity": self.free_cash_flow_to_equity,
            "free_cash_flow_to_firm": self.free_cash_flow_to_firm,
            "tangible_asset_value": self.tangible_asset_value,
            "net_current_asset_value": self.net_current_asset_value,
        }

    def __repr__(self):
        return f"<CompanyKeyMetrics(symbol={self.symbol}, date={self.date})>"


class CompanyDiscountedCashFlow(Base):
    """Discounted Cash Flow (DCF) valuation for a company"""

    __tablename__ = "company_dcf"
    __table_args__ = (
        UniqueConstraint("company_id", name="uq_dcf_company"),
        Index("ix_dcf_symbol_date", "symbol", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    dcf: Mapped[float | None] = mapped_column(Float, nullable=True)
    stock_price: Mapped[float | None] = mapped_column(Float, nullable=True)
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
        back_populates="discounted_cash_flow",
        foreign_keys=[company_id],
        lazy="select",
        uselist=False,
    )

    def __repr__(self):
        return f"<CompanyDiscountedCashFlow(symbol={self.symbol}, date={self.date})>"


class CompanyRevenueProductSegmentation(Base):
    """Revenue breakdown by product or business segment"""

    __tablename__ = "company_revenue_product_segmentations"
    __table_args__ = (
        UniqueConstraint("symbol", "fiscal_year", "period", name="uq_revenue_segment"),
        Index("ix_segment_symbol_year", "symbol", "fiscal_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True, nullable=False)

    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[str] = mapped_column(
        String(10), nullable=False
    )  # FY, Q1, Q2, Q3, Q4
    date: Mapped[date_type] = mapped_column(Date, nullable=False)

    # Store all product segments as JSON
    # Example: {"Mac": 33708000000, "Service": 109158000000, ...}
    segments_data: Mapped[str] = mapped_column(Text, nullable=False)

    # Optional currency field
    reported_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="revenue_product_segmentations",
        foreign_keys=[company_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyRevenueProductSegmentation(symbol={self.symbol}, fiscal_year={self.fiscal_year}, period={self.period})>"
