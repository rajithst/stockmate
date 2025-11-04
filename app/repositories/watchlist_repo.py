import logging
from typing import TYPE_CHECKING

from sqlalchemy import func as sql_func
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.company import Company
from app.db.models.quote import StockPrice
from app.db.models.watchlist import Watchlist, WatchlistItem
from app.repositories.base_repo import BaseRepository
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistItemCreate,
    WatchlistUpdate,
)

if TYPE_CHECKING:
    from app.db.models.company import Company
    from app.db.models.financial_ratio import CompanyFinancialRatio

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

    def load_current_prices_for_items(
        self, items: list[WatchlistItem]
    ) -> dict[str, float]:
        """
        Bulk load current prices for all items to avoid N+1 queries.

        Returns a dict mapping symbol -> current_price
        """

        if not items:
            return {}

        symbols = list({item.symbol for item in items})

        # Get the most recent price for each symbol in a single query
        stmt = (
            select(
                StockPrice.symbol, sql_func.max(StockPrice.date).label("latest_date")
            )
            .where(StockPrice.symbol.in_(symbols))
            .group_by(StockPrice.symbol)
        )

        latest_dates = {row[0]: row[1] for row in self._db.execute(stmt).all()}

        if not latest_dates:
            return {symbol: 0.0 for symbol in symbols}

        # Get the prices for those latest dates
        stmt = (
            select(StockPrice)
            .where(StockPrice.symbol.in_(symbols))
            .order_by(StockPrice.symbol, StockPrice.date.desc())
        )

        results = self._db.execute(stmt).scalars().all()
        prices = {}
        seen_symbols = set()
        for result in results:
            if result.symbol not in seen_symbols:
                prices[result.symbol] = result.close_price
                seen_symbols.add(result.symbol)

        # Fill in missing symbols with 0.0
        for symbol in symbols:
            if symbol not in prices:
                prices[symbol] = 0.0

        return prices

    def load_company_profiles_for_items(
        self, items: list[WatchlistItem]
    ) -> dict[str, "Company | None"]:
        """
        Bulk load company profiles for all items to avoid N+1 queries.

        Returns a dict mapping symbol -> Company
        """

        if not items:
            return {}

        symbols = list({item.symbol for item in items})

        # Get all companies in a single query
        stmt = select(Company).where(Company.symbol.in_(symbols))
        results = self._db.execute(stmt).scalars().all()

        profiles = {company.symbol: company for company in results}

        # Fill in missing symbols with None
        for symbol in symbols:
            if symbol not in profiles:
                profiles[symbol] = None

        return profiles

    def load_financial_ratios_for_items(
        self, items: list[WatchlistItem]
    ) -> dict[str, "CompanyFinancialRatio | None"]:
        """
        Bulk load latest financial ratios for all items to avoid N+1 queries.

        Returns a dict mapping symbol -> CompanyFinancialRatio
        """
        from app.db.models.financial_ratio import CompanyFinancialRatio

        if not items:
            return {}

        symbols = list({item.symbol for item in items})
        ratios = {}

        # Priority: FY > Q4 > Q3 > Q2 > Q1
        periods = ["FY", "Q4", "Q3", "Q2", "Q1"]

        for symbol in symbols:
            for period in periods:
                # Get the latest fiscal year for this symbol and period
                stmt = (
                    select(CompanyFinancialRatio)
                    .where(
                        CompanyFinancialRatio.symbol == symbol,
                        CompanyFinancialRatio.period == period,
                    )
                    .order_by(
                        CompanyFinancialRatio.fiscal_year.desc(),
                        CompanyFinancialRatio.date.desc(),
                    )
                    .limit(1)
                )

                result = self._db.execute(stmt).scalar_one_or_none()
                if result:
                    ratios[symbol] = result
                    break

            # Fill in missing symbol with None
            if symbol not in ratios:
                ratios[symbol] = None

        return ratios
