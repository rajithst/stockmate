from sqlalchemy import DateTime, Float, Date
from app.db.engine import Base
from sqlalchemy import ForeignKey, String, func, UniqueConstraint, Index

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date as date_type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyTechnicalIndicator(Base):
    __tablename__ = "company_technical_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    simple_moving_average: Mapped[float] = mapped_column(Float, nullable=True)
    exponential_moving_average: Mapped[float] = mapped_column(Float, nullable=True)
    weighted_moving_average: Mapped[float] = mapped_column(Float, nullable=True)
    double_exponential_moving_average: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    triple_exponential_moving_average: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    relative_strength_index: Mapped[float] = mapped_column(Float, nullable=True)
    standard_deviation: Mapped[float] = mapped_column(Float, nullable=True)
    williams_percent_r: Mapped[float] = mapped_column(Float, nullable=True)
    average_directional_index: Mapped[float] = mapped_column(Float, nullable=True)
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
        UniqueConstraint(
            "company_id", "date", name="uq_technical_indicator_company_date"
        ),
        Index("ix_technical_indicator_symbol_date", "symbol", "date"),
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="technical_indicators",
        foreign_keys=[company_id],
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<TechnicalIndicator(symbol={self.symbol}, date={self.date}, simple_moving_average={self.simple_moving_average})>"
