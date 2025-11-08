"""
Financial Statement Models

Contains all financial statement related models:
- CompanyIncomeStatement: P&L statement data
- CompanyBalanceSheet: Balance sheet data
- CompanyCashFlowStatement: Cash flow statement data
- CompanyFinancialRatio: Calculated financial ratios
"""

from datetime import date as date_type, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Date,
    Float,
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


class CompanyIncomeStatement(Base):
    """Income Statement (P&L) for a company"""

    __tablename__ = "company_income_statements"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "fiscal_year", "period", name="uq_income_period"
        ),
        Index("ix_income_symbol_date", "symbol", "date"),
        Index("ix_income_fiscal_year", "fiscal_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
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
    period: Mapped[str] = mapped_column(String(5))

    # Revenue and cost
    revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    cost_of_revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    gross_profit: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Operating expenses
    research_and_development_expenses: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    general_and_administrative_expenses: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    selling_and_marketing_expenses: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    selling_general_and_administrative_expenses: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    other_expenses: Mapped[float | None] = mapped_column(Float, nullable=True)
    operating_expenses: Mapped[float | None] = mapped_column(Float, nullable=True)
    cost_and_expenses: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Interest income/expense
    net_interest_income: Mapped[float | None] = mapped_column(Float, nullable=True)
    interest_income: Mapped[float | None] = mapped_column(Float, nullable=True)
    interest_expense: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Depreciation & amortization
    depreciation_and_amortization: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # Profit metrics
    ebitda: Mapped[float | None] = mapped_column(Float, nullable=True)
    ebit: Mapped[float | None] = mapped_column(Float, nullable=True)
    non_operating_income_excluding_interest: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    operating_income: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Other income/expenses & taxes
    total_other_income_expenses_net: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    income_before_tax: Mapped[float | None] = mapped_column(Float, nullable=True)
    income_tax_expense: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Net income details
    net_income_from_continuing_operations: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_income_from_discontinued_operations: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    other_adjustments_to_net_income: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_income: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_income_deductions: Mapped[float | None] = mapped_column(Float, nullable=True)
    bottom_line_net_income: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Earnings per share
    eps: Mapped[float | None] = mapped_column(nullable=True)
    eps_diluted: Mapped[float | None] = mapped_column(nullable=True)
    weighted_average_shs_out: Mapped[float | None] = mapped_column(Float, nullable=True)
    weighted_average_shs_out_dil: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
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
        back_populates="income_statements",
        foreign_keys=[company_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyIncomeStatement(symbol={self.symbol}, date={self.date})>"


class CompanyBalanceSheet(Base):
    """Balance Sheet for a company"""

    __tablename__ = "company_balance_sheets"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "fiscal_year", "period", name="uq_balance_sheet_period"
        ),
        Index("ix_balance_sheet_symbol_date", "symbol", "date"),
        Index("ix_balance_sheet_fiscal_year", "fiscal_year"),
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
    period: Mapped[str] = mapped_column(String(5))

    # Current Assets
    cash_and_cash_equivalents: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    short_term_investments: Mapped[float | None] = mapped_column(Float, nullable=True)
    cash_and_short_term_investments: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_receivables: Mapped[float | None] = mapped_column(Float, nullable=True)
    accounts_receivables: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_receivables: Mapped[float | None] = mapped_column(Float, nullable=True)
    inventory: Mapped[float | None] = mapped_column(Float, nullable=True)
    prepaids: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_current_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_current_assets: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Non-Current Assets
    property_plant_equipment_net: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    goodwill: Mapped[float | None] = mapped_column(Float, nullable=True)
    intangible_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    goodwill_and_intangible_assets: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    long_term_investments: Mapped[float | None] = mapped_column(Float, nullable=True)
    tax_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_non_current_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_non_current_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_assets: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Current Liabilities
    total_payables: Mapped[float | None] = mapped_column(Float, nullable=True)
    account_payables: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_payables: Mapped[float | None] = mapped_column(Float, nullable=True)
    accrued_expenses: Mapped[float | None] = mapped_column(Float, nullable=True)
    short_term_debt: Mapped[float | None] = mapped_column(Float, nullable=True)
    capital_lease_obligations_current: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    tax_payables: Mapped[float | None] = mapped_column(Float, nullable=True)
    deferred_revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_current_liabilities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    total_current_liabilities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # Non-Current Liabilities
    long_term_debt: Mapped[float | None] = mapped_column(Float, nullable=True)
    deferred_revenue_non_current: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    deferred_tax_liabilities_non_current: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    other_non_current_liabilities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    total_non_current_liabilities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    other_liabilities: Mapped[float | None] = mapped_column(Float, nullable=True)
    capital_lease_obligations: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    total_liabilities: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Stockholders' Equity
    treasury_stock: Mapped[float | None] = mapped_column(Float, nullable=True)
    preferred_stock: Mapped[float | None] = mapped_column(Float, nullable=True)
    common_stock: Mapped[float | None] = mapped_column(Float, nullable=True)
    retained_earnings: Mapped[float | None] = mapped_column(Float, nullable=True)
    additional_paid_in_capital: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    accumulated_other_comprehensive_income_loss: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    other_total_stockholders_equity: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    total_stockholders_equity: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    total_equity: Mapped[float | None] = mapped_column(Float, nullable=True)
    minority_interest: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Totals & Debt
    total_liabilities_and_total_equity: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    total_investments: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_debt: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_debt: Mapped[float | None] = mapped_column(Float, nullable=True)
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
        back_populates="balance_sheets",
        foreign_keys=[company_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyBalanceSheet(symbol={self.symbol}, date={self.date})>"


class CompanyCashFlowStatement(Base):
    """Cash Flow Statement for a company"""

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
    net_income: Mapped[float | None] = mapped_column(Float, nullable=True)
    depreciation_and_amortization: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    deferred_income_tax: Mapped[float | None] = mapped_column(Float, nullable=True)
    stock_based_compensation: Mapped[float | None] = mapped_column(Float, nullable=True)
    change_in_working_capital: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    accounts_receivables: Mapped[float | None] = mapped_column(Float, nullable=True)
    inventory: Mapped[float | None] = mapped_column(Float, nullable=True)
    accounts_payables: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_working_capital: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_non_cash_items: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_cash_provided_by_operating_activities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # Investing Activities
    investments_in_property_plant_and_equipment: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    acquisitions_net: Mapped[float | None] = mapped_column(Float, nullable=True)
    purchases_of_investments: Mapped[float | None] = mapped_column(Float, nullable=True)
    sales_maturities_of_investments: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    other_investing_activities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_cash_provided_by_investing_activities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # Financing Activities
    net_debt_issuance: Mapped[float | None] = mapped_column(Float, nullable=True)
    long_term_net_debt_issuance: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    short_term_net_debt_issuance: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_stock_issuance: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_common_stock_issuance: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    common_stock_issuance: Mapped[float | None] = mapped_column(Float, nullable=True)
    common_stock_repurchased: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_preferred_stock_issuance: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_dividends_paid: Mapped[float | None] = mapped_column(Float, nullable=True)
    common_dividends_paid: Mapped[float | None] = mapped_column(Float, nullable=True)
    preferred_dividends_paid: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_financing_activities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_cash_provided_by_financing_activities: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # Other Adjustments
    effect_of_forex_changes_on_cash: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_change_in_cash: Mapped[float | None] = mapped_column(Float, nullable=True)
    cash_at_end_of_period: Mapped[float | None] = mapped_column(Float, nullable=True)
    cash_at_beginning_of_period: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    operating_cash_flow: Mapped[float | None] = mapped_column(Float, nullable=True)
    capital_expenditure: Mapped[float | None] = mapped_column(Float, nullable=True)
    free_cash_flow: Mapped[float | None] = mapped_column(Float, nullable=True)
    income_taxes_paid: Mapped[float | None] = mapped_column(Float, nullable=True)
    interest_paid: Mapped[float | None] = mapped_column(Float, nullable=True)
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


class CompanyFinancialRatio(Base):
    """Financial Ratios for a company"""

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
