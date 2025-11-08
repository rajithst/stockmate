from datetime import datetime, date as date_type
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    func,
    UniqueConstraint,
    Index,
    Date,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyStockSplit(Base):
    __tablename__ = "company_stock_splits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    numerator: Mapped[int] = mapped_column(nullable=False)
    denominator: Mapped[int] = mapped_column(nullable=False)
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
        UniqueConstraint("company_id", "date", name="uq_stock_split_company_date"),
        Index("ix_stock_split_symbol_date", "symbol", "date"),
    )

    # Relationship
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="stock_splits",
        foreign_keys=[company_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<CompanyStockSplit(symbol={self.symbol}, date={self.date}, ratio={self.numerator}:{self.denominator})>"


class CompanyStockPeer(Base):
    __tablename__ = "company_stock_peers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    company_name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float, nullable=True)
    market_cap: Mapped[float] = mapped_column(Float, nullable=True)
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
        UniqueConstraint("company_id", "symbol", name="uq_stock_peer_company_symbol"),
        Index("ix_stock_peer_symbol", "symbol"),
    )

    company: Mapped["Company"] = relationship(
        back_populates="stock_peers", foreign_keys=[company_id], lazy="select"
    )

    def __repr__(self):
        return f"<CompanyStockPeer(symbol={self.symbol}, company_name={self.company_name}, price={self.price})>"
