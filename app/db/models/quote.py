from datetime import date as date_type, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    func,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class IndexQuote(Base):
    """Latest quote data for market indices (^GSPC, ^DJI, ^IXIC, etc.)"""

    __tablename__ = "index_quotes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(
        String(20), index=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    change: Mapped[float] = mapped_column(Float, nullable=True)
    change_percent: Mapped[float] = mapped_column(Float, nullable=True)
    open_price: Mapped[float] = mapped_column(Float, nullable=False)
    previous_close_price: Mapped[float] = mapped_column(Float, nullable=False)
    day_high_price: Mapped[float] = mapped_column(Float, nullable=False)
    day_low_price: Mapped[float] = mapped_column(Float, nullable=False)
    year_high_price: Mapped[float] = mapped_column(Float, nullable=True)
    year_low_price: Mapped[float] = mapped_column(Float, nullable=True)
    price_average_50d: Mapped[float] = mapped_column(Float, nullable=True)
    price_average_200d: Mapped[float] = mapped_column(Float, nullable=True)
    volume: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (Index("ix_index_quote_symbol", "symbol"),)


class CompanyStockPriceChange(Base):
    __tablename__ = "stock_price_changes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True, nullable=False)

    # Performance data for different time periods
    one_day: Mapped[float] = mapped_column(Float, nullable=True)
    five_day: Mapped[float] = mapped_column(Float, nullable=True)
    one_month: Mapped[float] = mapped_column(Float, nullable=True)
    three_month: Mapped[float] = mapped_column(Float, nullable=True)
    six_month: Mapped[float] = mapped_column(Float, nullable=True)
    ytd: Mapped[float] = mapped_column(Float, nullable=True)
    one_year: Mapped[float] = mapped_column(Float, nullable=True)
    three_year: Mapped[float] = mapped_column(Float, nullable=True)
    five_year: Mapped[float] = mapped_column(Float, nullable=True)
    ten_year: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("company_id", name="uq_price_change_company"),
        Index("ix_price_change_symbol", "symbol"),
    )

    # Relationship to company
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="stock_price_change",
        foreign_keys=[company_id],
        lazy="select",
        uselist=False,
    )


class CompanyStockPrice(Base):
    __tablename__ = "stock_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True, nullable=False)
    date: Mapped[date_type] = mapped_column(DateTime, nullable=False)
    open_price: Mapped[float] = mapped_column(Float, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    high_price: Mapped[float] = mapped_column(Float, nullable=False)
    low_price: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(nullable=False)
    change: Mapped[float] = mapped_column(Float, nullable=True)
    change_percent: Mapped[float] = mapped_column(Float, nullable=True)
    after_hours_price: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("company_id", "date", name="uq_stock_price_company_date"),
        Index("ix_stock_price_symbol_date", "symbol", "date"),
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="stock_prices",
        foreign_keys=[company_id],
        lazy="select",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "company_id": self.company_id,
            "symbol": self.symbol,
            "date": self.date,
            "open_price": self.open_price,
            "close_price": self.close_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "volume": self.volume,
            "change": self.change,
            "change_percent": self.change_percent,
            "after_hours_price": self.after_hours_price,
        }
