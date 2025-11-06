from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# User Schemas
class User(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool = True
    last_login: Optional[datetime] = None
    last_password_change: Optional[datetime] = None
    theme_preference: str = "light"
    language_preference: str = "en"
    email_verified: bool = False
    two_factor_enabled: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Schema for user registration."""

    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserWrite(User):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(User):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Notification Preference Schemas
class NotificationPreference(BaseModel):
    user_id: int
    email_notifications: bool = True
    push_notifications: bool = False
    portfolio_alerts: bool = True
    price_alerts: bool = True
    daily_news_digest: bool = True
    weekly_report: bool = True

    model_config = ConfigDict(from_attributes=True)


class NotificationPreferenceWrite(NotificationPreference):
    model_config = ConfigDict(from_attributes=True)


class NotificationPreferenceRead(NotificationPreference):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
