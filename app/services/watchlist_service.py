from logging import getLogger

from sqlalchemy.orm import Session

from app.db.models.watchlist import WatchlistItem
from app.repositories.watchlist_repo import WatchlistItemRepository, WatchlistRepository
from app.schemas.watchlist import (
    WatchlistCompanyItem,
    WatchlistCreate,
    WatchlistItemCreate,
    WatchlistItemWrite,
    WatchlistRead,
    WatchlistUpdate,
    WatchlistUpsertRequest,
)

logger = getLogger(__name__)


class WatchlistService:
    def __init__(self, session: Session) -> None:
        self._repository = WatchlistRepository(session)

    def create_watchlist(
        self, watchlist_in: WatchlistUpsertRequest, user_id: int
    ) -> WatchlistRead:
        """Create a new watchlist for the authenticated user."""
        watchlist_data = watchlist_in.model_dump()
        watchlist_data["user_id"] = user_id
        watchlist_in = WatchlistCreate.model_validate(watchlist_data)
        watchlist = self._repository.create_watchlist(watchlist_in)
        return WatchlistRead.model_validate(watchlist)

    def update_watchlist(
        self, watchlist_id, watchlist_in: WatchlistUpsertRequest, user_id: int
    ) -> WatchlistRead:
        """Create or update a watchlist for the authenticated user."""
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            raise ValueError("Watchlist not found or access denied")

        watchlist_data = watchlist_in.model_dump()
        watchlist_data["id"] = watchlist_id
        watchlist_data["user_id"] = user_id
        watchlist_in = WatchlistUpdate.model_validate(watchlist_data)
        watchlist = self._repository.update_watchlist(watchlist_in)
        return WatchlistRead.model_validate(watchlist)

    def delete_watchlist(self, watchlist_id: int, user_id: int) -> None:
        """Delete a watchlist, ensuring it belongs to the authenticated user."""
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            raise ValueError("Watchlist not found or access denied")

        self._repository.delete_watchlist(watchlist_id, user_id)
        logger.info(f"Deleted watchlist with ID: {watchlist_id}")


class WatchListItemService:
    def __init__(self, session: Session) -> None:
        self._repository = WatchlistItemRepository(session)

    @staticmethod
    def _watchlist_item_to_company_item(
        item: WatchlistItem,
    ) -> WatchlistCompanyItem | None:
        """Convert a WatchlistItem to a WatchlistCompanyItem schema."""
        company = item.company_profile
        if not company:
            return WatchlistCompanyItem(
                symbol=item.symbol,
                company_name="",
                price=item.current_price,
                currency=getattr(company, "currency", "USD"),
                price_change=0.0,
                price_change_percent=0.0,
                market_cap=0.0,
            )

        # Safely extract metrics with fallback to defaults
        financial_ratios = item.financial_ratios or {}

        return WatchlistCompanyItem(
            symbol=company.symbol,
            company_name=company.company_name,
            price=item.current_price,
            currency=company.currency,
            price_change=company.daily_price_change or 0.0,
            price_change_percent=company.daily_price_change_percent or 0.0,
            market_cap=company.market_cap,
            price_to_earnings_ratio=getattr(
                financial_ratios, "price_to_earnings_ratio", None
            ),
            price_to_earnings_growth_ratio=getattr(
                financial_ratios, "price_to_earnings_growth_ratio", None
            ),
            forward_price_to_earnings_growth_ratio=getattr(
                financial_ratios, "forward_price_to_earnings_growth_ratio", None
            ),
            price_to_book_ratio=getattr(financial_ratios, "price_to_book_ratio", None),
            price_to_sales_ratio=getattr(
                financial_ratios, "price_to_sales_ratio", None
            ),
            price_to_free_cash_flow_ratio=getattr(
                financial_ratios, "price_to_free_cash_flow_ratio", None
            ),
            price_to_operating_cash_flow_ratio=getattr(
                financial_ratios, "price_to_operating_cash_flow_ratio", None
            ),
            image=company.image,
        )

    def get_watchlist_items(
        self, watchlist_id: int, user_id: int
    ) -> list[WatchlistCompanyItem]:
        """Get all items for a watchlist, ensuring it belongs to the authenticated user."""
        # Verify the user owns the watchlist
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            raise ValueError("Watchlist not found or access denied")

        watchlist_items = self._repository.get_watchlist_items(watchlist_id)

        result = []
        for item in watchlist_items:
            company_item = self._watchlist_item_to_company_item(item)
            if company_item:
                result.append(company_item)

        return result

    def get_watchlist_item(
        self, watchlist_id: int, symbol: str, user_id: int
    ) -> WatchlistCompanyItem | None:
        """Get a specific item from a watchlist by symbol, ensuring it belongs to the authenticated user."""
        # Verify the user owns the watchlist
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            raise ValueError("Watchlist not found or access denied")

        watchlist_item = self._repository.get_watchlist_item(watchlist_id, symbol)
        if watchlist_item:
            return self._watchlist_item_to_company_item(watchlist_item)

        return None

    def add_watchlist_item(
        self, watchlist_id: int, watchlist_item_in: WatchlistItemWrite, user_id: int
    ) -> WatchlistCompanyItem:
        """Add an item to a watchlist, ensuring it belongs to the authenticated user."""
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            logger.error("Watchlist not found or access denied")
            raise ValueError("Watchlist not found or access denied")
        watchlist_item_data = watchlist_item_in.model_dump()
        watchlist_item_data["watchlist_id"] = watchlist_id
        watchlist_item_in = WatchlistItemCreate.model_validate(watchlist_item_data)
        watchlist_item = self._repository.add_watchlist_item(watchlist_item_in)
        if watchlist_item:
            return self._watchlist_item_to_company_item(watchlist_item)
        return None

    def delete_watchlist_item(
        self, watchlist_id: int, watchlist_item_id: int, user_id: int
    ) -> None:
        """Delete a watchlist item, ensuring it belongs to the authenticated user's watchlist."""
        self._repository.delete_watchlist_item(watchlist_id, watchlist_item_id, user_id)
        logger.info(f"Deleted watchlist item with ID: {watchlist_item_id}")
