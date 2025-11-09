from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from app.db.models.portfolio import Portfolio

if TYPE_CHECKING:
    from app.db.models.notification import Notification, NotificationPreference
    from app.db.models.portfolio import Portfolio
    from app.db.models.watchlist import Watchlist


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_password_change: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    theme_preference: Mapped[str] = mapped_column(
        String(20), nullable=False, default="light"
    )
    language_preference: Mapped[str] = mapped_column(
        String(10), nullable=False, default="en"
    )
    email_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    two_factor_enabled: Mapped[bool] = mapped_column(nullable=False, default=False)
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
    portfolios: Mapped[list["Portfolio"]] = relationship(
        "Portfolio",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    watchlists: Mapped[list["Watchlist"]] = relationship(
        "Watchlist",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    notification_preferences: Mapped["NotificationPreference | None"] = relationship(
        "NotificationPreference",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
        uselist=False,
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    email_notifications: Mapped[bool] = mapped_column(nullable=False, default=True)
    push_notifications: Mapped[bool] = mapped_column(nullable=False, default=False)
    portfolio_alerts: Mapped[bool] = mapped_column(nullable=False, default=True)
    price_alerts: Mapped[bool] = mapped_column(nullable=False, default=True)
    daily_news_digest: Mapped[bool] = mapped_column(nullable=False, default=True)
    weekly_report: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship
    user: Mapped["User"] = relationship(
        "User",
        back_populates="notification_preferences",
        foreign_keys=[user_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<NotificationPreference(user_id={self.user_id}, email_notifications={self.email_notifications})>"
