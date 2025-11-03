from datetime import date as date_type, datetime

from sqlalchemy import Date, DateTime, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.engine import Base


class CompanyDividend(Base):
    __tablename__ = "company_dividends"
    __table_args__ = (
        UniqueConstraint("symbol", "date", name="uq_dividend_date"),
        Index("ix_dividend_symbol_date", "symbol", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    record_date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    payment_date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    declaration_date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    adj_dividend: Mapped[float | None] = mapped_column(nullable=True)
    dividend: Mapped[float | None] = mapped_column(nullable=True)
    dividend_yield: Mapped[float | None] = mapped_column(nullable=True)
    frequency: Mapped[str | None] = mapped_column(String(20), nullable=True)
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
        return f"<CompanyDividend(symbol={self.symbol}, date={self.date}, dividend={self.dividend})>"
