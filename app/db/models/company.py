from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, object_session, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company_metrics import CompanyAnalystEstimate
    from app.db.models.financial_statements import CompanyBalanceSheet
    from app.db.models.financial_statements import CompanyCashFlowStatement
    from app.db.models.company_metrics import CompanyDiscountedCashFlow
    from app.db.models.financial_health import CompanyFinancialHealth
    from app.db.models.financial_statements import CompanyFinancialRatio
    from app.db.models.financial_score import CompanyFinancialScore
    from app.db.models.grading import CompanyGrading, CompanyGradingSummary
    from app.db.models.financial_statements import CompanyIncomeStatement
    from app.db.models.company_metrics import CompanyKeyMetrics
    from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary
    from app.db.models.quote import CompanyStockPrice, CompanyStockPriceChange
    from app.db.models.ratings import CompanyRatingSummary
    from app.db.models.company_metrics import (
        CompanyRevenueProductSegmentation,
    )
    from app.db.models.stock import CompanyStockPeer, CompanyStockSplit
    from app.db.models.technical_indicators import CompanyTechnicalIndicator


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        Index("ix_company_symbol_exchange", "symbol", "exchange"),
        Index("ix_company_sector_industry", "sector", "industry"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(
        String(250), unique=True, index=True, nullable=False
    )
    company_name: Mapped[str] = mapped_column(String(250), nullable=False)

    # Core company data
    market_cap: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(50), nullable=False, default="USD")

    # Exchange info
    exchange_full_name: Mapped[str] = mapped_column(String(250), nullable=False)
    exchange: Mapped[str] = mapped_column(String(250), nullable=False, index=True)

    # Classification
    industry: Mapped[str | None] = mapped_column(String(250), nullable=True)
    sector: Mapped[str | None] = mapped_column(String(250), nullable=True, index=True)

    # Company details
    website: Mapped[str | None] = mapped_column(String(250), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(String(250), nullable=True)
    ipo_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Contact info
    country: Mapped[str | None] = mapped_column(String(250), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(250), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    zip: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    # Relationships - Collections of related objects
    analyst_estimates: Mapped[list["CompanyAnalystEstimate"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    revenue_product_segmentations: Mapped[list["CompanyRevenueProductSegmentation"]] = (
        relationship(
            back_populates="company", cascade="all, delete-orphan", lazy="select"
        )
    )
    stock_splits: Mapped[list["CompanyStockSplit"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    income_statements: Mapped[list["CompanyIncomeStatement"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    balance_sheets: Mapped[list["CompanyBalanceSheet"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    cash_flow_statements: Mapped[list["CompanyCashFlowStatement"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    gradings: Mapped[list["CompanyGrading"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    key_metrics: Mapped[list["CompanyKeyMetrics"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    financial_ratios: Mapped[list["CompanyFinancialRatio"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    stock_peers: Mapped[list["CompanyStockPeer"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    stock_prices: Mapped[list["CompanyStockPrice"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    financial_health: Mapped[list["CompanyFinancialHealth"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    technical_indicators: Mapped[list["CompanyTechnicalIndicator"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )

    grading_summary: Mapped["CompanyGradingSummary | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",  # Don't join by default
    )
    rating_summary: Mapped["CompanyRatingSummary | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",  # Don't join by default
    )
    price_target_summary: Mapped["CompanyPriceTargetSummary | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",  # Don't join by default
    )
    discounted_cash_flow: Mapped["CompanyDiscountedCashFlow | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",  # Don't join by default
    )
    price_target: Mapped["CompanyPriceTarget | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",  # Don't join by default
    )
    stock_price_change: Mapped["CompanyStockPriceChange | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",  # Don't join by default
    )
    financial_score: Mapped["CompanyFinancialScore | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",  # Don't join by default
    )

    @property
    def latest_stock_price(self) -> "CompanyStockPrice | None":
        """
        Efficiently fetch only the most recent stock price without loading all prices.

        Note: This executes a query each time but only fetches one record.
        Since stock prices are accessed frequently together (price, change, volume),
        the single query is more efficient than loading all historical prices.
        SQLAlchemy's session-level identity map will cache the CompanyStockPrice instance.
        """
        session = object_session(self)
        if not session:
            return None

        from app.db.models.quote import CompanyStockPrice

        return (
            session.query(CompanyStockPrice)
            .filter(CompanyStockPrice.company_id == self.id)
            .order_by(CompanyStockPrice.date.desc())
            .limit(1)
            .first()
        )

    @property
    def price(self) -> float:
        """Get the current/latest closing price from stock_prices table."""
        latest = self.latest_stock_price
        return latest.close_price if latest else 0.0

    @property
    def daily_price_change(self) -> float | None:
        """Calculate daily price change from latest stock price."""
        latest = self.latest_stock_price
        return latest.change if latest else None

    @property
    def daily_price_change_percent(self) -> float | None:
        """Calculate daily price change percentage from latest stock price."""
        latest = self.latest_stock_price
        return latest.change_percent if latest else None

    @property
    def open_price(self) -> float | None:
        """Get today's opening price."""
        latest = self.latest_stock_price
        return latest.open_price if latest else None

    @property
    def high_price(self) -> float | None:
        """Get today's high price."""
        latest = self.latest_stock_price
        return latest.high_price if latest else None

    @property
    def low_price(self) -> float | None:
        """Get today's low price."""
        latest = self.latest_stock_price
        return latest.low_price if latest else None

    @property
    def volume(self) -> int | None:
        """Get today's trading volume."""
        latest = self.latest_stock_price
        return latest.volume if latest else None

    def __repr__(self) -> str:
        return f"<Company(symbol={self.symbol}, name={self.company_name})>"


class NonUSCompany(Base):
    """Non-US company data from YFinance

    Stores comprehensive company information for international stocks,
    including pricing, valuations, financials, and analyst data.
    """

    __tablename__ = "non_us_companies"
    __table_args__ = (
        Index("ix_non_us_company_symbol_exchange", "symbol", "exchange"),
        Index("ix_non_us_company_sector_industry", "sector", "industry"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # === BASIC COMPANY INFORMATION ===
    symbol: Mapped[str] = mapped_column(
        String(250), unique=True, index=True, nullable=False
    )
    short_name: Mapped[str] = mapped_column(String(250), default="", nullable=False)
    long_name: Mapped[str] = mapped_column(String(250), nullable=False)
    quote_type: Mapped[str] = mapped_column(
        String(50), default="EQUITY", nullable=False
    )

    # === LOCATION & CONTACT ===
    country: Mapped[str | None] = mapped_column(String(250), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address1: Mapped[str | None] = mapped_column(String(250), nullable=True)
    address2: Mapped[str | None] = mapped_column(String(250), nullable=True)
    zip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ir_website: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # === COMPANY CLASSIFICATION ===
    industry: Mapped[str | None] = mapped_column(String(250), nullable=True, index=True)
    industry_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    industry_display: Mapped[str | None] = mapped_column(String(250), nullable=True)
    sector: Mapped[str | None] = mapped_column(String(250), nullable=True, index=True)
    sector_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sector_display: Mapped[str | None] = mapped_column(String(250), nullable=True)

    # === COMPANY DESCRIPTION & DETAILS ===
    long_business_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_time_employees: Mapped[float | None] = mapped_column(Float, nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    default_image: Mapped[bool | None] = mapped_column(nullable=True)

    # === EXCHANGE INFORMATION ===
    exchange: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    full_exchange_name: Mapped[str] = mapped_column(String(250), nullable=False)
    market: Mapped[str | None] = mapped_column(String(50), nullable=True)
    market_state: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # === IPO & TRADING INFO ===
    ipo_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # === PRICING INFORMATION ===
    currency: Mapped[str] = mapped_column(String(10), nullable=False)
    current_price: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    previous_close: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    open: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    day_low: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    day_high: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    regular_market_previous_close: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    regular_market_open: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    regular_market_day_low: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    regular_market_day_high: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    regular_market_price: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    regular_market_change: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    regular_market_change_percent: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    bid: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    ask: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    bid_size: Mapped[float | None] = mapped_column(Float, nullable=True)
    ask_size: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_hint: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === VOLUME INFORMATION ===
    volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    regular_market_volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_volume_10_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_daily_volume_10_day: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    average_daily_volume_3_month: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # === MARKET CAPITALIZATION & SHARES ===
    market_cap: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    enterprise_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    shares_outstanding: Mapped[float | None] = mapped_column(Float, nullable=True)
    implied_shares_outstanding: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    float_shares: Mapped[float | None] = mapped_column(Float, nullable=True)
    held_percent_insiders: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    held_percent_institutions: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )

    # === 52 WEEK INFORMATION ===
    fifty_two_week_low: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    fifty_two_week_high: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    fifty_two_week_low_change: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    fifty_two_week_low_change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    fifty_two_week_high_change: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    fifty_two_week_high_change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    fifty_two_week_range: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fifty_two_week_change: Mapped[float | None] = mapped_column(Float, nullable=True)
    fifty_two_week_change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # === ALL TIME HIGH/LOW ===
    all_time_high: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    all_time_low: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )

    # === MOVING AVERAGES ===
    fifty_day_average: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    fifty_day_average_change: Mapped[float | None] = mapped_column(Float, nullable=True)
    fifty_day_average_change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    two_hundred_day_average: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    two_hundred_day_average_change: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    two_hundred_day_average_change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # === DIVIDEND INFORMATION ===
    dividend_rate: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    dividend_yield: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    trailing_annual_dividend_rate: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    trailing_annual_dividend_yield: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    five_year_avg_dividend_yield: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    ex_dividend_date: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_dividend_date: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_dividend_value: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    payout_ratio: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )

    # === VALUATION RATIOS ===
    trailing_pe: Mapped[float | None] = mapped_column(Float, nullable=True)
    forward_pe: Mapped[float | None] = mapped_column(Float, nullable=True)
    trailing_peg_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_to_sales_trailing_12_months: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    price_to_book: Mapped[float | None] = mapped_column(Float, nullable=True)
    enterprise_to_revenue: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === EARNINGS & EPS ===
    trailing_eps: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    forward_eps: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    eps_trailing_twelve_months: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    eps_for_forward: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    earnings_growth: Mapped[float | None] = mapped_column(Float, nullable=True)
    earnings_quarterly_growth: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    net_income_to_common: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === FINANCIAL METRICS ===
    book_value: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    total_cash: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    total_cash_per_share: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    total_debt: Mapped[float | None] = mapped_column(Float, default=0.0, nullable=True)
    total_revenue: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    revenue_per_share: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    gross_profits: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    beta: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === PROFITABILITY & MARGINS ===
    profit_margins: Mapped[float | None] = mapped_column(Float, nullable=True)
    gross_margins: Mapped[float | None] = mapped_column(Float, nullable=True)
    operating_margins: Mapped[float | None] = mapped_column(Float, nullable=True)
    ebitda_margins: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === RETURNS ===
    return_on_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_on_equity: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === GROWTH ===
    revenue_growth: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === ANALYST INFORMATION ===
    number_of_analyst_opinions: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    recommendation_key: Mapped[str | None] = mapped_column(String(50), nullable=True)
    recommendation_mean: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_analyst_rating: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    target_mean_price: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    target_median_price: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    target_high_price: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )
    target_low_price: Mapped[float | None] = mapped_column(
        Float, default=0.0, nullable=True
    )

    # === FISCAL YEAR INFORMATION ===
    last_fiscal_year_end: Mapped[float | None] = mapped_column(Float, nullable=True)
    next_fiscal_year_end: Mapped[float | None] = mapped_column(Float, nullable=True)
    most_recent_quarter: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === EARNINGS CALL INFORMATION ===
    earnings_timestamp: Mapped[float | None] = mapped_column(Float, nullable=True)
    earnings_timestamp_start: Mapped[float | None] = mapped_column(Float, nullable=True)
    earnings_timestamp_end: Mapped[float | None] = mapped_column(Float, nullable=True)
    earnings_call_timestamp_start: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    earnings_call_timestamp_end: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    is_earnings_date_estimate: Mapped[bool | None] = mapped_column(nullable=True)

    # === STOCK SPLIT INFORMATION ===
    last_split_factor: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_split_date: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === GOVERNANCE & RISK ===
    audit_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    board_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    compensation_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    share_holder_rights_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    overall_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    governance_epoch_date: Mapped[float | None] = mapped_column(Float, nullable=True)
    compensation_as_of_epoch_date: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    # === MISCELLANEOUS ===
    quote_source_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    triggerable: Mapped[bool | None] = mapped_column(nullable=True)
    custom_price_alert_confidence: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    source_interval: Mapped[float | None] = mapped_column(Float, nullable=True)
    exchange_data_delayed_by: Mapped[float | None] = mapped_column(Float, nullable=True)
    message_board_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    has_pre_post_market_data: Mapped[bool | None] = mapped_column(nullable=True)
    esg_populated: Mapped[bool | None] = mapped_column(nullable=True)
    region: Mapped[str | None] = mapped_column(String(50), nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    type_display: Mapped[str | None] = mapped_column(String(100), nullable=True)
    regular_market_day_range: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    regular_market_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    sand_p_52_week_change: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_age: Mapped[float | None] = mapped_column(Float, nullable=True)

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<NonUSCompany(symbol={self.symbol}, name={self.long_name})>"
