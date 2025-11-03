import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.watchlist import Watchlist, WatchlistItem
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistItemCreate,
    WatchlistUpdate,
)
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class WatchlistRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def verify_watchlist_ownership(self, watchlist_id: int, user_id: int) -> bool:
        """Verify that a watchlist belongs to a specific user."""
        try:
            watchlist = self._get_by_filter(
                Watchlist, {"id": watchlist_id, "user_id": user_id}
            )
            return len(watchlist) > 0
        except SQLAlchemyError as e:
            logger.error(f"Error verifying watchlist ownership: {e}")
            raise

    def get_watchlist_by_id(self, watchlist_id: int) -> Watchlist | None:
        """Get a watchlist by its ID."""
        return self._get_by_filter(Watchlist, {"id": watchlist_id})

    def create_watchlist(self, watchlist_in: WatchlistCreate) -> Watchlist:
        """Create a new watchlist."""
        return self._upsert_single(
            watchlist_in, Watchlist, lambda w: {"id": None}, "create_watchlist"
        )

    def update_watchlist(self, watchlist_in: WatchlistUpdate) -> Watchlist:
        """Create or update a watchlist."""

        return self._upsert_single(
            watchlist_in,
            Watchlist,
            lambda w: {"id": w.id},
            "update_watchlist",
        )

    def delete_watchlist(self, watchlist_id: int, user_id: int) -> bool:
        """Delete a watchlist, ensuring it belongs to the user."""
        return self._delete_by_filter(
            Watchlist, {"id": watchlist_id, "user_id": user_id}, "delete_watchlist"
        )


class WatchlistItemRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def verify_watchlist_ownership(self, watchlist_id: int, user_id: int) -> bool:
        """Verify that a watchlist belongs to a specific user."""
        try:
            watchlist = self._get_by_filter(
                Watchlist, {"id": watchlist_id, "user_id": user_id}
            )
            return len(watchlist) > 0
        except SQLAlchemyError as e:
            logger.error(f"Error verifying watchlist ownership: {e}")
            raise

    def get_watchlist_items(self, watchlist_id: int) -> list[WatchlistItem]:
        """Get all items in a watchlist."""
        return self._get_by_filter(WatchlistItem, {"watchlist_id": watchlist_id})

    def get_watchlist_item(
        self, watchlist_id: int, symbol: str
    ) -> WatchlistItem | None:
        """Get a watchlist item by its symbol."""
        return self._get_by_filter(
            WatchlistItem, {"watchlist_id": watchlist_id, "symbol": symbol}
        )

    def add_watchlist_item(
        self, watchlist_item_in: WatchlistItemCreate
    ) -> WatchlistItem:
        """Add an item to a watchlist."""
        return self._upsert_single(
            watchlist_item_in,
            WatchlistItem,
            lambda w: {"id": None},
            "add_watchlist_item",
        )

    def delete_watchlist_item(
        self, watchlist_id: int, watchlist_item_id: int, user_id: int
    ) -> bool:
        """Delete a watchlist item, ensuring it belongs to a user's watchlist."""
        return self._delete_by_join(
            WatchlistItem,
            Watchlist,
            [
                WatchlistItem.id == watchlist_item_id,
                Watchlist.user_id == user_id,
                Watchlist.id == watchlist_id,
            ],
            "delete_watchlist_item",
        )
