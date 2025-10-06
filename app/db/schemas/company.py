from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class Company(Base):
    __tablename__ = "company"

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
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    sector: Mapped[str] = mapped_column(String(250), nullable=True)
    country: Mapped[str] = mapped_column(String(250), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(250), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    zip: Mapped[str] = mapped_column(String(20), nullable=True)
    image: Mapped[str] = mapped_column(String(250), nullable=True)
    ipo_date: Mapped[str] = mapped_column(String(50), nullable=True)

    # Relationships
    dividends: Mapped[list["CompanyDividend"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    stock_splits: Mapped[list["CompanyStockSplit"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    income_statements: Mapped[list["CompanyIncomeStatement"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    balance_sheets: Mapped[list["CompanyBalanceSheet"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    cash_flow_statements: Mapped[list["CompanyCashFlowStatement"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    ratings: Mapped[list["CompanyRating"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    gradings: Mapped[list["CompanyGrading"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    grading_summary: Mapped["CompanyGradingSummary"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan"
    )
    financial_score: Mapped["CompanyFinancialScores"] = relationship(
        back_populates="company",
        uselist=False,  # 1:1 mapping
        cascade="all, delete-orphan"
    )
    general_news: Mapped[list["CompanyGeneralNews"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    price_target_news: Mapped[list["CompanyPriceTargetNews"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    grading_news: Mapped[list["CompanyGradingNews"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    key_metrics: Mapped[list["CompanyKeyMetrics"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    financial_ratios: Mapped[list["CompanyFinancialRatios"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    stock_peers: Mapped[list["CompanyStockPeer"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CompanyProfile(symbol={self.symbol}, name={self.company_name})>"
