"""Data Transfer Objects (DTOs) for repository layer responses.

These DTOs provide type-safe, explicit contracts for data returned from repositories.
They prevent lazy-loading issues and decouple the service layer from ORM models.
"""

from datetime import datetime

from pydantic import BaseModel


class PortfolioCreateDTO(BaseModel):
    """DTO for created portfolio response."""

    id: int
    user_id: int
    name: str
    description: str | None
    currency: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PortfolioUpdateDTO(BaseModel):
    """DTO for updated portfolio response."""

    id: int
    user_id: int
    name: str
    description: str | None
    currency: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WatchlistCreateDTO(BaseModel):
    """DTO for created watchlist response."""

    id: int
    user_id: int
    name: str
    currency: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WatchlistUpdateDTO(BaseModel):
    """DTO for updated watchlist response."""

    id: int
    user_id: int
    name: str
    currency: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
