from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class DiscountedCashFlow(Base):
    __tablename__ = "company_dcf"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    date: Mapped[str] = mapped_column(String(20), nullable=True)
    dcf: Mapped[Float] = mapped_column(Float, nullable=True)
    stock_price: Mapped[Float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationship to company profile
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="discounted_cash_flow",
        foreign_keys=[company_id],
        lazy="joined",
        uselist=False,
    )

    def __repr__(self):
        return f"<DiscountedCashFlow(symbol={self.symbol}, date={self.date})>"
