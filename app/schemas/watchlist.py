from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# Watchlist Schemas
class Watchlist(BaseModel):
    user_id: int
    name: str
    currency: str = "USD"
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WatchlistWrite(Watchlist):
    model_config = ConfigDict(from_attributes=True)


class WatchlistRead(Watchlist):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Watchlist Item Schemas
class WatchlistItem(BaseModel):
    watchlist_id: int
    symbol: str

    model_config = ConfigDict(from_attributes=True)


class WatchlistItemWrite(WatchlistItem):
    model_config = ConfigDict(from_attributes=True)


class WatchlistItemRead(WatchlistItem):
    id: int
    added_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Composite Response Schema
class WatchlistDetailRead(WatchlistRead):
    items: List[WatchlistItemRead] = []

    model_config = ConfigDict(from_attributes=True)
