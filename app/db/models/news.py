from datetime import datetime

from sqlalchemy import String, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class CompanyGeneralNews(Base):
    __tablename__ = "company_general_news"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), index=True, nullable=True
    )
    symbol: Mapped[str] = mapped_column(String(12), nullable=True, index=True)

    published_date: Mapped[datetime] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(1000), nullable=True)
    site: Mapped[str] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(back_populates="general_news")

    def __repr__(self):
        return f"<CompanyGeneralNews(symbol={self.symbol}, title={self.title})>"


class CompanyPriceTargetNews(Base):
    __tablename__ = "company_price_target_news"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    published_date: Mapped[datetime] = mapped_column(nullable=False)
    news_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    news_title: Mapped[str] = mapped_column(String(500), nullable=False)
    analyst_name: Mapped[str] = mapped_column(String(255), nullable=False)
    price_target: Mapped[float] = mapped_column(nullable=False)
    adj_price_target: Mapped[float] = mapped_column(nullable=True)
    price_when_posted: Mapped[float] = mapped_column(nullable=False)
    news_publisher: Mapped[str] = mapped_column(String(255), nullable=True)
    news_base_url: Mapped[str] = mapped_column(String(500), nullable=True)
    analyst_company: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(back_populates="price_target_news")

    def __repr__(self):
        return (
            f"<CompanyPriceTargetNews(symbol={self.symbol}, title={self.news_title})>"
        )


class CompanyGradingNews(Base):
    __tablename__ = "company_grading_news"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    published_date: Mapped[datetime] = mapped_column(nullable=False)
    news_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    news_title: Mapped[str] = mapped_column(String(500), nullable=False)
    news_base_url: Mapped[str] = mapped_column(String(500), nullable=True)
    news_publisher: Mapped[str] = mapped_column(String(255), nullable=True)
    new_grade: Mapped[str] = mapped_column(String(10), nullable=False)
    previous_grade: Mapped[str] = mapped_column(String(10), nullable=True)
    grading_company: Mapped[str] = mapped_column(String(255), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=True)
    price_when_posted: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    company: Mapped["Company"] = relationship(back_populates="grading_news")

    def __repr__(self):
        return f"<CompanyGradingNews(symbol={self.symbol}, title={self.news_title})>"
