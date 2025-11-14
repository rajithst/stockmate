from logging import getLogger

from sqlalchemy.orm import Session

from app.repositories.watchlist_repo import WatchlistRepository
from app.schemas.user import (
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

    def get_user_watchlists(self, user_id: int) -> list[WatchlistRead]:
        """Get all watchlists for a specific user."""
        watchlists = self._repository.get_all_watchlists(user_id)
        return [WatchlistRead.model_validate(watchlist) for watchlist in watchlists]

    def create_watchlist(
        self, watchlist_in: WatchlistUpsertRequest, user_id: int
    ) -> WatchlistRead:
        """Create a new watchlist for the authenticated user."""
        watchlist_in = WatchlistCreate(
            name=watchlist_in.name,
            currency=watchlist_in.currency,
            description=watchlist_in.description,
            user_id=user_id,
        )
        watchlist_dto = self._repository.create_watchlist(watchlist_in)
        logger.info(f"Created watchlist {watchlist_dto.id} for user {user_id}")
        return WatchlistRead(
            id=watchlist_dto.id,
            name=watchlist_dto.name,
            currency=watchlist_dto.currency,
            description=watchlist_dto.description,
            created_at=watchlist_dto.created_at,
            updated_at=watchlist_dto.updated_at,
        )

    def update_watchlist(
        self, watchlist_id, watchlist_in: WatchlistUpsertRequest, user_id: int
    ) -> WatchlistRead:
        """Update a watchlist for the authenticated user."""
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            raise ValueError("Watchlist not found or access denied")

        watchlist = WatchlistUpdate(
            id=watchlist_id,
            name=watchlist_in.name,
            currency=watchlist_in.currency,
            description=watchlist_in.description,
            user_id=user_id,
        )
        watchlist_dto = self._repository.update_watchlist(watchlist, user_id)
        logger.info(f"Updated watchlist {watchlist_dto.id} for user {user_id}")
        return WatchlistRead(
            id=watchlist_dto.id,
            name=watchlist_dto.name,
            currency=watchlist_dto.currency,
            description=watchlist_dto.description,
            created_at=watchlist_dto.created_at,
            updated_at=watchlist_dto.updated_at,
        )

    def delete_watchlist(self, watchlist_id: int, user_id: int) -> None:
        """Delete a watchlist, ensuring it belongs to the authenticated user."""
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            raise ValueError("Watchlist not found or access denied")

        self._repository.delete_watchlist(watchlist_id, user_id)
        logger.info(f"Deleted watchlist with ID: {watchlist_id}")

    def _convert_watchlist_item_to_company_item(
        self, item: any
    ) -> WatchlistCompanyItem | None:
        """Convert a WatchlistItem to WatchlistCompanyItem with company details."""
        if not item or not item.company_profile:
            return None

        # Safely extract financial ratio fields with None defaults
        financial_ratios = item.financial_ratios or {}
        company_profile = item.company_profile or {}
        logger.info(f"Company profile for {item.symbol}: {company_profile}")
        logger.info(f"Financial ratios for {item.symbol}: {financial_ratios}")

        item_in = WatchlistCompanyItem(
            id=item.id,
            symbol=item.symbol,
            company_name=company_profile.get("company_name", None),
            price=item.current_price,
            currency=company_profile.get("currency", None),
            price_change=item.price_change,
            price_change_percent=item.price_change_percent,
            market_cap=company_profile.get("market_cap", None),
            price_to_earnings_ratio=financial_ratios.get(
                "price_to_earnings_ratio", None
            ),
            price_to_earnings_growth_ratio=financial_ratios.get(
                "price_to_earnings_growth_ratio", None
            ),
            forward_price_to_earnings_growth_ratio=financial_ratios.get(
                "forward_price_to_earnings_growth_ratio", None
            ),
            price_to_book_ratio=financial_ratios.get("price_to_book_ratio", None),
            price_to_sales_ratio=financial_ratios.get("price_to_sales_ratio", None),
            price_to_free_cash_flow_ratio=financial_ratios.get(
                "price_to_free_cash_flow_ratio", None
            ),
            price_to_operating_cash_flow_ratio=financial_ratios.get(
                "price_to_operating_cash_flow_ratio", None
            ),
            image=company_profile.get("image", None),
        )
        return item_in

    def get_watchlist_items(
        self, watchlist_id: int, user_id: int
    ) -> list[WatchlistCompanyItem]:
        """Get all items for a watchlist, ensuring it belongs to the authenticated user."""
        # Verify the user owns the watchlist
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            raise ValueError("Watchlist not found or access denied")

        watchlist = self._repository.get_watchlist_with_relations(watchlist_id, user_id)
        if not watchlist:
            return []

        result = []
        watchlist_items = list(watchlist.items)
        for item in watchlist_items:
            if not item.company_profile:
                continue
            result.append(self._convert_watchlist_item_to_company_item(item))
        return result

    def add_watchlist_item(
        self, watchlist_id: int, watchlist_item_in: WatchlistItemWrite, user_id: int
    ) -> WatchlistCompanyItem | None:
        """Add an item to a watchlist, ensuring it belongs to the authenticated user."""
        if not self._repository.verify_watchlist_ownership(watchlist_id, user_id):
            logger.error("Watchlist not found or access denied")
            raise ValueError("Watchlist not found or access denied")

        if self._repository.check_watchlist_item_exists(
            watchlist_id, watchlist_item_in.symbol
        ):
            logger.error("Watchlist item already exists")
            raise ValueError("Watchlist item already exists")

        watchlist_item_in = WatchlistItemCreate(
            watchlist_id=watchlist_id,
            symbol=watchlist_item_in.symbol,
        )
        watchlist_item = self._repository.add_watchlist_item(watchlist_item_in)
        if watchlist_item:
            # Load the item with all relations pre-loaded
            result = self._repository.get_watchlist_item_with_relations(
                watchlist_id, watchlist_item.id, user_id
            )
            return self._convert_watchlist_item_to_company_item(result)
        return None

    def delete_watchlist_item(
        self, watchlist_id: int, watchlist_item_id: int, user_id: int
    ) -> None:
        """Delete a watchlist item, ensuring it belongs to the authenticated user's watchlist."""
        self._repository.delete_watchlist_item(watchlist_id, watchlist_item_id, user_id)
        logger.info(f"Deleted watchlist item with ID: {watchlist_item_id}")
