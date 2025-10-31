from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class Watchlist(Base):
    __tablename__ = "watchlists"

    id = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name = mapped_column(String(100), nullable=False)
    currency = mapped_column(String(10), nullable=False, default="USD")
    description = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="watchlists", foreign_keys=[user_id], lazy="joined"
    )

    def __repr__(self):
        return f"<Watchlist(name={self.name}, user_id={self.user_id})>"


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = mapped_column(primary_key=True, autoincrement=True)
    watchlist_id = mapped_column(
        ForeignKey("watchlists.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol = mapped_column(String(12), index=True, nullable=False)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    watchlist: Mapped["Watchlist"] = relationship(
        "Watchlist", back_populates="items", foreign_keys=[watchlist_id], lazy="joined"
    )

    def __repr__(self):
        return (
            f"<WatchlistItem(symbol={self.symbol}, watchlist_id={self.watchlist_id})>"
        )
