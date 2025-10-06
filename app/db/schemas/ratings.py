from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyRating(Base):
    __tablename__ = "company_ratings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    rating: Mapped[str] = mapped_column(String(50), nullable=True)
    overall_score: Mapped[int] = mapped_column(nullable=True)
    discounted_cash_flow_score: Mapped[int] = mapped_column(nullable=True)
    return_on_equity_score: Mapped[int] = mapped_column(nullable=True)
    return_on_assets_score: Mapped[int] = mapped_column(nullable=True)
    debt_to_equity_score: Mapped[int] = mapped_column(nullable=True)
    price_to_earnings_score: Mapped[int] = mapped_column(nullable=True)
    price_to_book_score: Mapped[int] = mapped_column(nullable=True)

    company: Mapped["CompanyProfile"] = relationship(back_populates="ratings")

    def __repr__(self):
        return f"<CompanyRating(symbol={self.symbol}, rating={self.rating}, overall_score={self.overall_score})>"
