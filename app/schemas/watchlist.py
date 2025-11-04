from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Watchlist Schemas
class Watchlist(BaseModel):
    name: str
    currency: str = "USD"
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WatchlistUpsertRequest(Watchlist):
    model_config = ConfigDict(from_attributes=True)


class WatchlistCreate(Watchlist):
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class WatchlistUpdate(Watchlist):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class WatchlistRead(Watchlist):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Watchlist Item Schemas
class WatchlistItem(BaseModel):
    symbol: str

    model_config = ConfigDict(from_attributes=True)


class WatchlistItemWrite(WatchlistItem):
    model_config = ConfigDict(from_attributes=True)


class WatchlistItemCreate(WatchlistItem):
    watchlist_id: int
    model_config = ConfigDict(from_attributes=True)


class WatchlistCompanyItem(BaseModel):
    symbol: str
    company_name: str
    price: float
    currency: str
    price_change: float
    price_change_percent: float
    market_cap: float
    price_to_earnings_ratio: Optional[float] = None
    price_to_earnings_growth_ratio: Optional[float] = None
    forward_price_to_earnings_growth_ratio: Optional[float] = None
    price_to_book_ratio: Optional[float] = None
    price_to_sales_ratio: Optional[float] = None
    price_to_free_cash_flow_ratio: Optional[float] = None
    price_to_operating_cash_flow_ratio: Optional[float] = None
    image: Optional[str] = None


class WatchlistResponse(BaseModel):
    watchlist: WatchlistRead
    items: list[WatchlistCompanyItem] = []

    model_config = ConfigDict(from_attributes=True)
