from datetime import date as date_type

from sqlalchemy import Date, func
from sqlalchemy import Float, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.engine import Base


class CompanyEarningsCalendar(Base):
    __tablename__ = "company_earnings_calendar"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    eps_actual: Mapped[float] = mapped_column(Float, nullable=True)
    eps_estimated: Mapped[float] = mapped_column(Float, nullable=True)
    revenue_actual: Mapped[float] = mapped_column(Float, nullable=True)
    revenue_estimated: Mapped[float] = mapped_column(Float, nullable=True)
    last_update: Mapped[date_type] = mapped_column(Date, nullable=True)
    created_at = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self):
        return f"<CompanyEarningsCalendar(symbol={self.symbol}, date={self.date}, eps_actual={self.eps_actual}, eps_estimated={self.eps_estimated}, revenue_actual={self.revenue_actual}, revenue_estimated={self.revenue_estimated})>"
