from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class StockPriceChange(Base):
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

    # Relationship to company
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="price_change",
        foreign_keys=[company_id],
        lazy="joined",
        uselist=False,
    )


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    open_price: Mapped[float] = mapped_column(Float, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    high_price: Mapped[float] = mapped_column(Float, nullable=False)
    low_price: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(nullable=False)
    change: Mapped[float] = mapped_column(Float, nullable=True)
    change_percent: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="stock_prices",
        foreign_keys=[company_id],
        lazy="joined",
    )
