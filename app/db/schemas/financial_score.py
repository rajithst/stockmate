from sqlalchemy import String, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.engine import Base

class CompanyFinancialScores(Base):
    __tablename__ = "company_financial_scores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company_profiles.id", ondelete="CASCADE"), index=True)
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

    # Relationship to company
    company: Mapped["CompanyProfile"] = relationship(back_populates="company_financial_scores")

    __table_args__ = (
        Index("ix_company_financial_scores_symbol", "symbol"),
    )

    def __repr__(self):
        return f"<CompanyFinancialScores(symbol={self.symbol})>"
