from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyFinancialRatios(Base):
    __tablename__ = "company_financial_ratios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), index=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=True)
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=True)
    period: Mapped[str] = mapped_column(String(10), nullable=True)
    reported_currency: Mapped[str] = mapped_column(String(10), nullable=True)

    # Profitability margins
    gross_profit_margin: Mapped[float] = mapped_column(nullable=True)
    ebit_margin: Mapped[float] = mapped_column(nullable=True)
    ebitda_margin: Mapped[float] = mapped_column(nullable=True)
    operating_profit_margin: Mapped[float] = mapped_column(nullable=True)
    pretax_profit_margin: Mapped[float] = mapped_column(nullable=True)
    continuous_operations_profit_margin: Mapped[float] = mapped_column(nullable=True)
    net_profit_margin: Mapped[float] = mapped_column(nullable=True)
    bottom_line_profit_margin: Mapped[float] = mapped_column(nullable=True)

    # Efficiency ratios
    receivables_turnover: Mapped[float] = mapped_column(nullable=True)
    payables_turnover: Mapped[float] = mapped_column(nullable=True)
    inventory_turnover: Mapped[float] = mapped_column(nullable=True)
    fixed_asset_turnover: Mapped[float] = mapped_column(nullable=True)
    asset_turnover: Mapped[float] = mapped_column(nullable=True)

    # Liquidity ratios
    current_ratio: Mapped[float] = mapped_column(nullable=True)
    quick_ratio: Mapped[float] = mapped_column(nullable=True)
    solvency_ratio: Mapped[float] = mapped_column(nullable=True)
    cash_ratio: Mapped[float] = mapped_column(nullable=True)

    # Valuation ratios
    price_to_earnings_ratio: Mapped[float] = mapped_column(nullable=True)
    price_to_earnings_growth_ratio: Mapped[float] = mapped_column(nullable=True)
    forward_price_to_earnings_growth_ratio: Mapped[float] = mapped_column(nullable=True)
    price_to_book_ratio: Mapped[float] = mapped_column(nullable=True)
    price_to_sales_ratio: Mapped[float] = mapped_column(nullable=True)
    price_to_free_cash_flow_ratio: Mapped[float] = mapped_column(nullable=True)
    price_to_operating_cash_flow_ratio: Mapped[float] = mapped_column(nullable=True)

    # Leverage ratios
    debt_to_assets_ratio: Mapped[float] = mapped_column(nullable=True)
    debt_to_equity_ratio: Mapped[float] = mapped_column(nullable=True)
    debt_to_capital_ratio: Mapped[float] = mapped_column(nullable=True)
    long_term_debt_to_capital_ratio: Mapped[float] = mapped_column(nullable=True)
    financial_leverage_ratio: Mapped[float] = mapped_column(nullable=True)

    # Cash flow coverage ratios
    working_capital_turnover_ratio: Mapped[float] = mapped_column(nullable=True)
    operating_cash_flow_ratio: Mapped[float] = mapped_column(nullable=True)
    operating_cash_flow_sales_ratio: Mapped[float] = mapped_column(nullable=True)
    free_cash_flow_operating_cash_flow_ratio: Mapped[float] = mapped_column(nullable=True)
    debt_service_coverage_ratio: Mapped[float] = mapped_column(nullable=True)
    interest_coverage_ratio: Mapped[float] = mapped_column(nullable=True)
    short_term_operating_cash_flow_coverage_ratio: Mapped[float] = mapped_column(nullable=True)
    operating_cash_flow_coverage_ratio: Mapped[float] = mapped_column(nullable=True)
    capital_expenditure_coverage_ratio: Mapped[float] = mapped_column(nullable=True)
    dividend_paid_and_capex_coverage_ratio: Mapped[float] = mapped_column(nullable=True)

    # Dividend ratios
    dividend_payout_ratio: Mapped[float] = mapped_column(nullable=True)
    dividend_yield: Mapped[float] = mapped_column(nullable=True)
    dividend_yield_percentage: Mapped[float] = mapped_column(nullable=True)

    # Per share metrics
    revenue_per_share: Mapped[float] = mapped_column(nullable=True)
    net_income_per_share: Mapped[float] = mapped_column(nullable=True)
    interest_debt_per_share: Mapped[float] = mapped_column(nullable=True)
    cash_per_share: Mapped[float] = mapped_column(nullable=True)
    book_value_per_share: Mapped[float] = mapped_column(nullable=True)
    tangible_book_value_per_share: Mapped[float] = mapped_column(nullable=True)
    shareholders_equity_per_share: Mapped[float] = mapped_column(nullable=True)
    operating_cash_flow_per_share: Mapped[float] = mapped_column(nullable=True)
    capex_per_share: Mapped[float] = mapped_column(nullable=True)
    free_cash_flow_per_share: Mapped[float] = mapped_column(nullable=True)

    # Misc ratios
    net_income_per_ebt: Mapped[float] = mapped_column(nullable=True)
    ebt_per_ebit: Mapped[float] = mapped_column(nullable=True)
    price_to_fair_value: Mapped[float] = mapped_column(nullable=True)
    debt_to_market_cap: Mapped[float] = mapped_column(nullable=True)
    effective_tax_rate: Mapped[float] = mapped_column(nullable=True)
    enterprise_value_multiple: Mapped[float] = mapped_column(nullable=True)

    # Relationship
    company: Mapped["Company"] = relationship(back_populates="financial_ratios")

    def __repr__(self):
        return f"<CompanyFinancialRatios(symbol={self.symbol}, date={self.date})>"
