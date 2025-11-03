from datetime import date as date_type, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    DateTime,
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


class DiscountedCashFlow(Base):
    __tablename__ = "company_dcf"
    __table_args__ = (
        UniqueConstraint("company_id", name="uq_dcf_company"),
        Index("ix_dcf_symbol_date", "symbol", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    dcf: Mapped[float | None] = mapped_column(Float, nullable=True)
    stock_price: Mapped[float | None] = mapped_column(Float, nullable=True)
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
        back_populates="discounted_cash_flow",
        foreign_keys=[company_id],
        lazy="select",
        uselist=False,
    )

    def __repr__(self):
        return f"<DiscountedCashFlow(symbol={self.symbol}, date={self.date})>"
