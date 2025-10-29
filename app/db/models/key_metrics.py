from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyKeyMetrics(Base):
    __tablename__ = "company_key_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=False)
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=False)
    period: Mapped[str] = mapped_column(String(10), nullable=False)
    reported_currency: Mapped[str] = mapped_column(String(10), nullable=False)

    # Market metrics
    market_cap: Mapped[int] = mapped_column(BigInteger, nullable=True)
    enterprise_value: Mapped[int] = mapped_column(BigInteger, nullable=True)
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
    working_capital: Mapped[int] = mapped_column(BigInteger, nullable=True)
    invested_capital: Mapped[int] = mapped_column(BigInteger, nullable=True)
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
    sales_general_and_administrative_to_revenue: Mapped[float] = mapped_column(
        nullable=True
    )
    research_and_development_to_revenue: Mapped[float] = mapped_column(nullable=True)
    stock_based_compensation_to_revenue: Mapped[float] = mapped_column(nullable=True)
    intangibles_to_total_assets: Mapped[float] = mapped_column(nullable=True)
    average_receivables: Mapped[int] = mapped_column(BigInteger, nullable=True)
    average_payables: Mapped[int] = mapped_column(BigInteger, nullable=True)
    average_inventory: Mapped[int] = mapped_column(BigInteger, nullable=True)
    days_of_sales_outstanding: Mapped[float] = mapped_column(nullable=True)
    days_of_payables_outstanding: Mapped[float] = mapped_column(nullable=True)
    days_of_inventory_outstanding: Mapped[float] = mapped_column(nullable=True)
    operating_cycle: Mapped[float] = mapped_column(nullable=True)
    cash_conversion_cycle: Mapped[float] = mapped_column(nullable=True)
    free_cash_flow_to_equity: Mapped[float] = mapped_column(nullable=True)
    free_cash_flow_to_firm: Mapped[float] = mapped_column(nullable=True)
    tangible_asset_value: Mapped[int] = mapped_column(BigInteger, nullable=True)
    net_current_asset_value: Mapped[int] = mapped_column(BigInteger, nullable=True)
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
        lazy="joined",
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
