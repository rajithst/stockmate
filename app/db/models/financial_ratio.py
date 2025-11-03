from datetime import date as date_type, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Date, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyFinancialRatio(Base):
    __tablename__ = "company_financial_ratios"
    __table_args__ = (
        UniqueConstraint("company_id", "fiscal_year", "period", name="uq_ratio_period"),
        Index("ix_ratio_symbol_date", "symbol", "date"),
        Index("ix_ratio_fiscal_year", "fiscal_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    fiscal_year: Mapped[int | None] = mapped_column(index=True, nullable=True)
    period: Mapped[str | None] = mapped_column(String(10), nullable=True)
    reported_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # Profitability margins
    gross_profit_margin: Mapped[float | None] = mapped_column(nullable=True)
    ebit_margin: Mapped[float | None] = mapped_column(nullable=True)
    ebitda_margin: Mapped[float | None] = mapped_column(nullable=True)
    operating_profit_margin: Mapped[float | None] = mapped_column(nullable=True)
    pretax_profit_margin: Mapped[float | None] = mapped_column(nullable=True)
    continuous_operations_profit_margin: Mapped[float | None] = mapped_column(
        nullable=True
    )
    net_profit_margin: Mapped[float | None] = mapped_column(nullable=True)
    bottom_line_profit_margin: Mapped[float | None] = mapped_column(nullable=True)

    # Efficiency ratios
    receivables_turnover: Mapped[float | None] = mapped_column(nullable=True)
    payables_turnover: Mapped[float | None] = mapped_column(nullable=True)
    inventory_turnover: Mapped[float | None] = mapped_column(nullable=True)
    fixed_asset_turnover: Mapped[float | None] = mapped_column(nullable=True)
    asset_turnover: Mapped[float | None] = mapped_column(nullable=True)

    # Liquidity ratios
    current_ratio: Mapped[float | None] = mapped_column(nullable=True)
    quick_ratio: Mapped[float | None] = mapped_column(nullable=True)
    solvency_ratio: Mapped[float | None] = mapped_column(nullable=True)
    cash_ratio: Mapped[float | None] = mapped_column(nullable=True)

    # Valuation ratios
    price_to_earnings_ratio: Mapped[float | None] = mapped_column(nullable=True)
    price_to_earnings_growth_ratio: Mapped[float | None] = mapped_column(nullable=True)
    forward_price_to_earnings_growth_ratio: Mapped[float | None] = mapped_column(
        nullable=True
    )
    price_to_book_ratio: Mapped[float | None] = mapped_column(nullable=True)
    price_to_sales_ratio: Mapped[float | None] = mapped_column(nullable=True)
    price_to_free_cash_flow_ratio: Mapped[float | None] = mapped_column(nullable=True)
    price_to_operating_cash_flow_ratio: Mapped[float | None] = mapped_column(
        nullable=True
    )

    # Leverage ratios
    debt_to_assets_ratio: Mapped[float | None] = mapped_column(nullable=True)
    debt_to_equity_ratio: Mapped[float | None] = mapped_column(nullable=True)
    debt_to_capital_ratio: Mapped[float | None] = mapped_column(nullable=True)
    long_term_debt_to_capital_ratio: Mapped[float | None] = mapped_column(nullable=True)
    financial_leverage_ratio: Mapped[float | None] = mapped_column(nullable=True)

    # Cash flow coverage ratios
    working_capital_turnover_ratio: Mapped[float | None] = mapped_column(nullable=True)
    operating_cash_flow_ratio: Mapped[float | None] = mapped_column(nullable=True)
    operating_cash_flow_sales_ratio: Mapped[float | None] = mapped_column(nullable=True)
    free_cash_flow_operating_cash_flow_ratio: Mapped[float | None] = mapped_column(
        nullable=True
    )
    debt_service_coverage_ratio: Mapped[float | None] = mapped_column(nullable=True)
    interest_coverage_ratio: Mapped[float | None] = mapped_column(nullable=True)
    short_term_operating_cash_flow_coverage_ratio: Mapped[float | None] = mapped_column(
        nullable=True
    )
    operating_cash_flow_coverage_ratio: Mapped[float | None] = mapped_column(
        nullable=True
    )
    capital_expenditure_coverage_ratio: Mapped[float | None] = mapped_column(
        nullable=True
    )
    dividend_paid_and_capex_coverage_ratio: Mapped[float | None] = mapped_column(
        nullable=True
    )

    # Dividend ratios
    dividend_payout_ratio: Mapped[float | None] = mapped_column(nullable=True)
    dividend_yield: Mapped[float | None] = mapped_column(nullable=True)
    dividend_yield_percentage: Mapped[float | None] = mapped_column(nullable=True)

    # Per share metrics
    revenue_per_share: Mapped[float | None] = mapped_column(nullable=True)
    net_income_per_share: Mapped[float | None] = mapped_column(nullable=True)
    interest_debt_per_share: Mapped[float | None] = mapped_column(nullable=True)
    cash_per_share: Mapped[float | None] = mapped_column(nullable=True)
    book_value_per_share: Mapped[float | None] = mapped_column(nullable=True)
    tangible_book_value_per_share: Mapped[float | None] = mapped_column(nullable=True)
    shareholders_equity_per_share: Mapped[float | None] = mapped_column(nullable=True)
    operating_cash_flow_per_share: Mapped[float | None] = mapped_column(nullable=True)
    capex_per_share: Mapped[float | None] = mapped_column(nullable=True)
    free_cash_flow_per_share: Mapped[float | None] = mapped_column(nullable=True)

    # Misc ratios
    net_income_per_ebt: Mapped[float | None] = mapped_column(nullable=True)
    ebt_per_ebit: Mapped[float | None] = mapped_column(nullable=True)
    price_to_fair_value: Mapped[float | None] = mapped_column(nullable=True)
    debt_to_market_cap: Mapped[float | None] = mapped_column(nullable=True)
    effective_tax_rate: Mapped[float | None] = mapped_column(nullable=True)
    enterprise_value_multiple: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    # Relationship
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="financial_ratios",
        foreign_keys=[company_id],
        lazy="select",
    )

    def to_dict(self):
        return {
            "gross_profit_margin": self.gross_profit_margin,
            "ebit_margin": self.ebit_margin,
            "ebitda_margin": self.ebitda_margin,
            "operating_profit_margin": self.operating_profit_margin,
            "pretax_profit_margin": self.pretax_profit_margin,
            "continuous_operations_profit_margin": self.continuous_operations_profit_margin,
            "net_profit_margin": self.net_profit_margin,
            "bottom_line_profit_margin": self.bottom_line_profit_margin,
            "receivables_turnover": self.receivables_turnover,
            "payables_turnover": self.payables_turnover,
            "inventory_turnover": self.inventory_turnover,
            "fixed_asset_turnover": self.fixed_asset_turnover,
            "asset_turnover": self.asset_turnover,
            "current_ratio": self.current_ratio,
            "quick_ratio": self.quick_ratio,
            "solvency_ratio": self.solvency_ratio,
            "cash_ratio": self.cash_ratio,
            "price_to_earnings_ratio": self.price_to_earnings_ratio,
            "price_to_earnings_growth_ratio": self.price_to_earnings_growth_ratio,
            "forward_price_to_earnings_growth_ratio": self.forward_price_to_earnings_growth_ratio,
            "price_to_book_ratio": self.price_to_book_ratio,
            "price_to_sales_ratio": self.price_to_sales_ratio,
            "price_to_free_cash_flow_ratio": self.price_to_free_cash_flow_ratio,
            "price_to_operating_cash_flow_ratio": self.price_to_operating_cash_flow_ratio,
            "debt_to_assets_ratio": self.debt_to_assets_ratio,
            "debt_to_equity_ratio": self.debt_to_equity_ratio,
            "debt_to_capital_ratio": self.debt_to_capital_ratio,
            "long_term_debt_to_capital_ratio": self.long_term_debt_to_capital_ratio,
            "financial_leverage_ratio": self.financial_leverage_ratio,
            "working_capital_turnover_ratio": self.working_capital_turnover_ratio,
            "operating_cash_flow_ratio": self.operating_cash_flow_ratio,
            "operating_cash_flow_sales_ratio": self.operating_cash_flow_sales_ratio,
            "free_cash_flow_operating_cash_flow_ratio": self.free_cash_flow_operating_cash_flow_ratio,
            "debt_service_coverage_ratio": self.debt_service_coverage_ratio,
            "interest_coverage_ratio": self.interest_coverage_ratio,
            "short_term_operating_cash_flow_coverage_ratio": self.short_term_operating_cash_flow_coverage_ratio,
            "operating_cash_flow_coverage_ratio": self.operating_cash_flow_coverage_ratio,
            "capital_expenditure_coverage_ratio": self.capital_expenditure_coverage_ratio,
            "dividend_paid_and_capex_coverage_ratio": self.dividend_paid_and_capex_coverage_ratio,
            "dividend_payout_ratio": self.dividend_payout_ratio,
            "dividend_yield": self.dividend_yield,
            "dividend_yield_percentage": self.dividend_yield_percentage,
            "revenue_per_share": self.revenue_per_share,
            "net_income_per_share": self.net_income_per_share,
            "interest_debt_per_share": self.interest_debt_per_share,
            "cash_per_share": self.cash_per_share,
            "book_value_per_share": self.book_value_per_share,
            "tangible_book_value_per_share": self.tangible_book_value_per_share,
            "shareholders_equity_per_share": self.shareholders_equity_per_share,
            "operating_cash_flow_per_share": self.operating_cash_flow_per_share,
            "capex_per_share": self.capex_per_share,
            "free_cash_flow_per_share": self.free_cash_flow_per_share,
            "net_income_per_ebt": self.net_income_per_ebt,
            "ebt_per_ebit": self.ebt_per_ebit,
            "price_to_fair_value": self.price_to_fair_value,
            "debt_to_market_cap": self.debt_to_market_cap,
            "effective_tax_rate": self.effective_tax_rate,
            "enterprise_value_multiple": self.enterprise_value_multiple,
        }

    def __repr__(self):
        return f"<CompanyFinancialRatios(symbol={self.symbol}, date={self.date})>"
