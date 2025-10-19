from typing import TYPE_CHECKING
from app.db.engine import Base
from sqlalchemy import Float, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyPriceTarget(Base):
    __tablename__ = "company_price_targets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    target_high: Mapped[float] = mapped_column(Float, nullable=True)
    target_low: Mapped[float] = mapped_column(Float, nullable=True)
    target_consensus: Mapped[float] = mapped_column(Float, nullable=True)
    target_median: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="price_target",
        foreign_keys=[company_id],
        lazy="joined",
        uselist=False,
    )

    def __repr__(self):
        return f"<CompanyPriceTarget(symbol={self.symbol}, target_high={self.target_high}, target_low={self.target_low}, target_consensus={self.target_consensus}, target_median={self.target_median})>"


class CompanyPriceTargetSummary(Base):
    __tablename__ = "company_price_target_summaries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    last_month_count: Mapped[int] = mapped_column(nullable=False)
    last_month_average_price_target: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    last_quarter_count: Mapped[int] = mapped_column(nullable=False)
    last_quarter_average_price_target: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    last_year_count: Mapped[int] = mapped_column(nullable=False)
    last_year_average_price_target: Mapped[float] = mapped_column(Float, nullable=False)
    all_time_count: Mapped[int] = mapped_column(nullable=False)
    all_time_average_price_target: Mapped[float] = mapped_column(Float, nullable=False)
    publishers: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="price_target_summary",
        foreign_keys=[company_id],
        lazy="joined",
        uselist=False,
    )

    def __repr__(self):
        return f"<CompanyPriceTargetSummary(symbol={self.symbol}, average_target={self.average_target}, number_of_analysts={self.number_of_analysts})>"
