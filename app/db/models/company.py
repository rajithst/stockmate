from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, object_session, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.balance_sheet import CompanyBalanceSheet
    from app.db.models.cashflow import CompanyCashFlowStatement
    from app.db.models.dcf import DiscountedCashFlow
    from app.db.models.financial_health import CompanyFinancialHealth
    from app.db.models.financial_ratio import CompanyFinancialRatio
    from app.db.models.financial_score import CompanyFinancialScore
    from app.db.models.grading import CompanyGrading, CompanyGradingSummary
    from app.db.models.income_statement import CompanyIncomeStatement
    from app.db.models.key_metrics import CompanyKeyMetrics
    from app.db.models.news import (
        CompanyGeneralNews,
        CompanyGradingNews,
        CompanyPriceTargetNews,
        CompanyStockNews,
    )
    from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary
    from app.db.models.quote import StockPrice, StockPriceChange
    from app.db.models.ratings import CompanyRatingSummary
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
    # Relationships - Collections (use selectin for better performance)
    stock_splits: Mapped[list["CompanyStockSplit"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    income_statements: Mapped[list["CompanyIncomeStatement"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    balance_sheets: Mapped[list["CompanyBalanceSheet"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    cash_flow_statements: Mapped[list["CompanyCashFlowStatement"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    gradings: Mapped[list["CompanyGrading"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    key_metrics: Mapped[list["CompanyKeyMetrics"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    financial_ratios: Mapped[list["CompanyFinancialRatio"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    stock_peers: Mapped[list["CompanyStockPeer"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    stock_prices: Mapped[list["StockPrice"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    financial_health: Mapped[list["CompanyFinancialHealth"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    technical_indicators: Mapped[list["CompanyTechnicalIndicator"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    general_news: Mapped[list["CompanyGeneralNews"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    price_target_news: Mapped[list["CompanyPriceTargetNews"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    grading_news: Mapped[list["CompanyGradingNews"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )
    stock_news: Mapped[list["CompanyStockNews"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="selectin"
    )

    # Relationships - One-to-One (use joined for immediate loading)
    grading_summary: Mapped["CompanyGradingSummary | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    rating_summary: Mapped["CompanyRatingSummary | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    price_target_summary: Mapped["CompanyPriceTargetSummary | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    discounted_cash_flow: Mapped["DiscountedCashFlow | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    price_target: Mapped["CompanyPriceTarget | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    stock_price_change: Mapped["StockPriceChange | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    financial_score: Mapped["CompanyFinancialScore | None"] = relationship(
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )

    @property
    def latest_stock_price(self) -> "StockPrice | None":
        """
        Efficiently fetch only the most recent stock price without loading all prices.

        Note: This executes a query each time but only fetches one record.
        Since stock prices are accessed frequently together (price, change, volume),
        the single query is more efficient than loading all historical prices.
        SQLAlchemy's session-level identity map will cache the StockPrice instance.
        """
        session = object_session(self)
        if not session:
            return None

        from app.db.models.quote import StockPrice

        return (
            session.query(StockPrice)
            .filter(StockPrice.company_id == self.id)
            .order_by(StockPrice.date.desc())
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

    @property
    def latest_key_metrics(self) -> "CompanyKeyMetrics | None":
        """
        Get the latest key metrics with fiscal year priority.

        Uses already-loaded key_metrics relationship (no additional queries).
        Priority: FY > Q4 > Q3 > Q2 > Q1 for the most recent fiscal year.
        """
        if not self.key_metrics:
            return None

        # Get the latest fiscal year from in-memory data
        latest_fiscal_year = max(metric.fiscal_year for metric in self.key_metrics)

        # Priority: FY > Q4 > Q3 > Q2 > Q1
        periods = ["FY", "Q4", "Q3", "Q2", "Q1"]
        for period in periods:
            for metric in self.key_metrics:
                if metric.fiscal_year == latest_fiscal_year and metric.period == period:
                    return metric

        return None

    def __repr__(self) -> str:
        return f"<Company(symbol={self.symbol}, name={self.company_name})>"
