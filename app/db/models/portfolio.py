from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    total_value: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_invested: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_gain_loss: Mapped[float] = mapped_column(nullable=False, default=0.0)
    dividends_received: Mapped[float] = mapped_column(nullable=False, default=0.0)
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
    user: Mapped["User"] = relationship(
        "User", back_populates="portfolios", foreign_keys=[user_id], lazy="joined"
    )
    sector_performances: Mapped[list["PortfolioSectorPerformance"]] = relationship(
        "PortfolioSectorPerformance",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    industry_performances: Mapped[list["PortfolioIndustryPerformance"]] = relationship(
        "PortfolioIndustryPerformance",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    holding_performances: Mapped[list["PortfolioHoldingPerformance"]] = relationship(
        "PortfolioHoldingPerformance",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    trading_histories: Mapped[list["PortfolioTradingHistory"]] = relationship(
        "PortfolioTradingHistory",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    dividend_histories: Mapped[list["PortfolioDividendHistory"]] = relationship(
        "PortfolioDividendHistory",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self):
        return f"<Portfolio(name={self.name}, user_id={self.user_id})>"


class PortfolioSectorPerformance(Base):
    __tablename__ = "portfolio_sector_performances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    allocation_percentage: Mapped[float] = mapped_column(nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    total_invested: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_gain_loss: Mapped[float] = mapped_column(nullable=False, default=0.0)
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
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="sector_performances",
        foreign_keys=[portfolio_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<PortfolioSectorPerformance(portfolio_id={self.portfolio_id}, sector={self.sector})>"


class PortfolioIndustryPerformance(Base):
    __tablename__ = "portfolio_industry_performances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    allocation_percentage: Mapped[float] = mapped_column(nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    total_invested: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_gain_loss: Mapped[float] = mapped_column(nullable=False, default=0.0)
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
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="industry_performances",
        foreign_keys=[portfolio_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<PortfolioIndustryPerformance(portfolio_id={self.portfolio_id}, industry={self.industry})>"


class PortfolioHoldingPerformance(Base):
    __tablename__ = "portfolio_holding_performances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    holding_symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    total_shares: Mapped[float] = mapped_column(nullable=False, default=0.0)
    allocation_percentage: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_invested: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_gain_loss: Mapped[float] = mapped_column(nullable=False, default=0.0)
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
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="holding_performances",
        foreign_keys=[portfolio_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<PortfolioHoldingPerformance(portfolio_id={self.portfolio_id}, holding_symbol={self.holding_symbol})>"


class PortfolioTradingHistory(Base):
    __tablename__ = "portfolio_trading_histories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    trade_type: Mapped[str] = mapped_column(String(10), nullable=False)  # BUY or SELL
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    shares: Mapped[float] = mapped_column(nullable=False, default=0.0)
    price_per_share: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_value: Mapped[float] = mapped_column(nullable=False, default=0.0)
    trade_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
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

    # Relationships
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="trading_histories",
        foreign_keys=[portfolio_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<PortfolioTradingHistory(portfolio_id={self.portfolio_id}, symbol={self.symbol}, trade_type={self.trade_type})>"


class PortfolioDividendHistory(Base):
    __tablename__ = "portfolio_dividend_histories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    shares: Mapped[float] = mapped_column(nullable=False, default=0.0)
    dividend_per_share: Mapped[float] = mapped_column(nullable=False, default=0.0)
    dividend_amount: Mapped[float] = mapped_column(nullable=False, default=0.0)
    declaration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
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

    # Relationships
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="dividend_histories",
        foreign_keys=[portfolio_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<PortfolioDividendHistory(portfolio_id={self.portfolio_id}, symbol={self.symbol}, dividend_amount={self.dividend_amount})>"
