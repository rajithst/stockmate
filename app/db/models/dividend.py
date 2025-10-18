from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyDividend(Base):
    __tablename__ = "company_dividends"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=False)
    record_date: Mapped[str] = mapped_column(String(20), nullable=True)
    payment_date: Mapped[str] = mapped_column(String(20), nullable=True)
    declaration_date: Mapped[str] = mapped_column(String(20), nullable=True)

    dividend: Mapped[float] = mapped_column(nullable=True)
    adj_dividend: Mapped[float] = mapped_column(nullable=True)
    dividend_yield: Mapped[float] = mapped_column(nullable=True)
    frequency: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationship
    company: Mapped["Company"] = relationship(back_populates="dividends")

    def __repr__(self):
        return f"<CompanyDividend(symbol={self.symbol}, date={self.date}, dividend={self.dividend})>"
