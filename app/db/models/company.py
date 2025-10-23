from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.financial_score import CompanyFinancialScores
    from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary
    from app.db.models.quote import StockPrice, StockPriceChange
    from app.db.models.ratings import CompanyRatingSummary
    from app.db.models.balance_sheet import CompanyBalanceSheet
    from app.db.models.cashflow import CompanyCashFlowStatement
    from app.db.models.dcf import DiscountedCashFlow
    from app.db.models.grading import CompanyGrading, CompanyGradingSummary
    from app.db.models.income_statement import CompanyIncomeStatement
    from app.db.models.key_metrics import (
        CompanyFinancialRatios,
        CompanyKeyMetrics,
    )
    from app.db.models.news import (
        CompanyGeneralNews,
        CompanyGradingNews,
        CompanyPriceTargetNews,
    )
    from app.db.models.stock import CompanyDividend, CompanyStockPeer, CompanyStockSplit


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(250), index=True)
    company_name: Mapped[str] = mapped_column(String(250), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    market_cap: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(50), nullable=False)
    exchange_full_name: Mapped[str] = mapped_column(String(250), nullable=False)
    exchange: Mapped[str] = mapped_column(String(250), nullable=False)
    industry: Mapped[str] = mapped_column(String(250), nullable=True)
    website: Mapped[str] = mapped_column(String(250), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    sector: Mapped[str] = mapped_column(String(250), nullable=True)
    country: Mapped[str] = mapped_column(String(250), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(250), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    zip: Mapped[str] = mapped_column(String(20), nullable=True)
    image: Mapped[str] = mapped_column(String(250), nullable=True)
    ipo_date: Mapped[str] = mapped_column(String(50), nullable=True)
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
    dividends: Mapped[list["CompanyDividend"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
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
    grading_summary: Mapped["CompanyGradingSummary"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan",
        lazy="select",
    )
    rating_summary: Mapped["CompanyRatingSummary"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan",
        lazy="select",
    )
    price_target_summary: Mapped["CompanyPriceTargetSummary"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan",
        lazy="select",
    )
    discounted_cash_flow: Mapped["DiscountedCashFlow"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan",
        lazy="select",
    )
    price_target: Mapped["CompanyPriceTarget"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan",
        lazy="select",
    )
    price_change: Mapped["StockPriceChange"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan",
        lazy="select",
    )
    financial_score: Mapped["CompanyFinancialScores"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan",
        lazy="select",
    )

    general_news: Mapped[list["CompanyGeneralNews"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    price_target_news: Mapped[list["CompanyPriceTargetNews"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    grading_news: Mapped[list["CompanyGradingNews"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    key_metrics: Mapped[list["CompanyKeyMetrics"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    financial_ratios: Mapped[list["CompanyFinancialRatios"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    stock_peers: Mapped[list["CompanyStockPeer"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )
    stock_prices: Mapped[list["StockPrice"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<CompanyProfile(symbol={self.symbol}, name={self.company_name})>"
