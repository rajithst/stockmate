from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.engine import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(12), nullable=True)

    published_date: Mapped[datetime] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(String(255), nullable=False)
    news_title: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    site: Mapped[str | None] = mapped_column(String(255), nullable=True)
    news_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    sentiment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self):
        return f"<News(symbol={self.symbol}, title={self.news_title})>"
