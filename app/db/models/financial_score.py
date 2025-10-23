from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.company import Company


class CompanyFinancialScores(Base):
    __tablename__ = "company_financial_scores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    reported_currency: Mapped[str] = mapped_column(String(10), nullable=True)
    altman_z_score: Mapped[float] = mapped_column(nullable=True)
    piotroski_score: Mapped[int] = mapped_column(nullable=True)
    working_capital: Mapped[float] = mapped_column(nullable=True)
    total_assets: Mapped[float] = mapped_column(nullable=True)
    retained_earnings: Mapped[float] = mapped_column(nullable=True)
    ebit: Mapped[float] = mapped_column(nullable=True)
    market_cap: Mapped[float] = mapped_column(nullable=True)
    total_liabilities: Mapped[float] = mapped_column(nullable=True)
    revenue: Mapped[float] = mapped_column(nullable=True)
    ccreated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    # Relationship to company
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="financial_score",
        foreign_keys=[company_id],
        lazy="joined",
        uselist=False,
    )

    def __repr__(self):
        return f"<CompanyFinancialScores(symbol={self.symbol})>"
