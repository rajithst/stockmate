from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyStockSplit(Base):
    __tablename__ = "company_stock_splits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(12), index=True)

    date: Mapped[str] = mapped_column(String(20), nullable=False)
    numerator: Mapped[int] = mapped_column(nullable=False)
    denominator: Mapped[int] = mapped_column(nullable=False)

    # Relationship
    company: Mapped["Company"] = relationship(back_populates="stock_splits")

    def __repr__(self):
        return f"<CompanyStockSplit(symbol={self.symbol}, date={self.date}, ratio={self.numerator}:{self.denominator})>"


class CompanyStockPeer(Base):
    __tablename__ = "company_stock_peers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), index=True, nullable=False)

    # Stock identification
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    company_name: Mapped[str] = mapped_column(String(255))

    # Stock metrics
    price: Mapped[float]
    market_cap: Mapped[int]

    company: Mapped["Company"] = relationship(back_populates="stock_peers")

    def __repr__(self):
        return f"<CompanyStockPeer(symbol={self.symbol}, company_name={self.company_name}, price={self.price})>"
