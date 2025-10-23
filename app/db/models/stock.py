from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
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
    date: Mapped[str] = mapped_column(String(20), nullable=False)
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

    # Relationship
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="stock_splits",
        foreign_keys=[company_id],
        lazy="joined",
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
    price: Mapped[float]
    market_cap: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(
        back_populates="stock_peers", foreign_keys=[company_id], lazy="joined"
    )

    def __repr__(self):
        return f"<CompanyStockPeer(symbol={self.symbol}, company_name={self.company_name}, price={self.price})>"
