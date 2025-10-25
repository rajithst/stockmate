from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
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
    adj_dividend: Mapped[float] = mapped_column(nullable=True)
    dividend: Mapped[float] = mapped_column(nullable=True)
    dividend_yield: Mapped[float] = mapped_column(nullable=True)
    frequency: Mapped[str] = mapped_column(String(20), nullable=True)
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
        back_populates="dividends",
        foreign_keys=[company_id],
        lazy="joined",
    )

    def __repr__(self):
        return f"<CompanyDividend(symbol={self.symbol}, date={self.date}, dividend={self.dividend})>"


class DividendCalendar(Base):
    __tablename__ = "dividend_calendars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=False)
    record_date: Mapped[str] = mapped_column(String(20), nullable=True)
    payment_date: Mapped[str] = mapped_column(String(20), nullable=True)
    declaration_date: Mapped[str] = mapped_column(String(20), nullable=True)
    adj_dividend: Mapped[float] = mapped_column(nullable=True)
    dividend: Mapped[float] = mapped_column(nullable=True)
    dividend_yield: Mapped[float] = mapped_column(nullable=True)
    frequency: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self):
        return f"<DividendCalendar(symbol={self.symbol}, date={self.date}, dividend={self.dividend})>"
