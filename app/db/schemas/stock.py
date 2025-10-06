from sqlalchemy import String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyStockSplit(Base):
    __tablename__ = "company_stock_splits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=False)
    numerator: Mapped[int] = mapped_column(nullable=False)
    denominator: Mapped[int] = mapped_column(nullable=False)

    # Relationship
    company: Mapped["Company"] = relationship(back_populates="stock_splits")

    __table_args__ = (
        UniqueConstraint("company_id", "date", name="uq_company_stocksplit_unique_date"),
        Index("ix_company_stocksplit_symbol", "symbol"),
    )

    def __repr__(self):
        return f"<CompanyStockSplit(symbol={self.symbol}, date={self.date}, ratio={self.numerator}:{self.denominator})>"


class CompanyStockPeer(Base):
    __tablename__ = "company_stock_peers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Stock identification
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    company_name: Mapped[str] = mapped_column(String(255))

    # Stock metrics
    price: Mapped[float]
    market_cap: Mapped[int]

    def __repr__(self):
        return f"<StockPeer(symbol={self.symbol}, company_name={self.company_name}, price={self.price})>"
