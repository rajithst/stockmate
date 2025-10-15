from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyGrading(Base):
    __tablename__ = "company_gradings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=False)
    grading_company: Mapped[str] = mapped_column(String(255), nullable=True)
    previous_grade: Mapped[str] = mapped_column(String(10), nullable=True)
    new_grade: Mapped[str] = mapped_column(String(10), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(back_populates="gradings")

    def __repr__(self):
        return f"<CompanyGrading(symbol={self.symbol}, new_grade={self.new_grade}, date={self.date})>"


class CompanyGradingSummary(Base):
    __tablename__ = "company_grading_summaries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    strong_buy: Mapped[int] = mapped_column(nullable=False)
    buy: Mapped[int] = mapped_column(nullable=False)
    hold: Mapped[int] = mapped_column(nullable=False)
    sell: Mapped[int] = mapped_column(nullable=False)
    strong_sell: Mapped[int] = mapped_column(nullable=False)
    consensus: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(back_populates="grading_summary")

    def __repr__(self):
        return (
            f"<CompanyGradingSummary(symbol={self.symbol}, consensus={self.consensus})>"
        )
