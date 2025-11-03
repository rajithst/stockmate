from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyRatingSummary(Base):
    __tablename__ = "company_rating_summaries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    rating: Mapped[str] = mapped_column(String(50), nullable=True)
    overall_score: Mapped[int] = mapped_column(nullable=True)
    discounted_cash_flow_score: Mapped[int] = mapped_column(nullable=True)
    return_on_equity_score: Mapped[int] = mapped_column(nullable=True)
    return_on_assets_score: Mapped[int] = mapped_column(nullable=True)
    debt_to_equity_score: Mapped[int] = mapped_column(nullable=True)
    price_to_earnings_score: Mapped[int] = mapped_column(nullable=True)
    price_to_book_score: Mapped[int] = mapped_column(nullable=True)
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
        UniqueConstraint("company_id", name="uq_rating_summary_company"),
        Index("ix_rating_summary_symbol", "symbol"),
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="rating_summary",
        foreign_keys=[company_id],
        lazy="select",
        uselist=False,
    )

    def __repr__(self):
        return f"<CompanyRatingSummary(symbol={self.symbol}, rating={self.rating}, overall_score={self.overall_score})>"
