import logging
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, lazyload

from app.db.models.company import Company
from app.db.models.quote import CompanyStockPrice
from app.db.models.watchlist import Watchlist, WatchlistItem
from app.schemas.user import (
    WatchlistCreate,
    WatchlistItemCreate,
    WatchlistUpdate,
)
from app.util.model_mapper import map_model

if TYPE_CHECKING:
    from app.db.models.company import Company

logger = logging.getLogger(__name__)


class WatchlistRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def verify_watchlist_ownership(self, watchlist_id: int, user_id: int) -> bool:
        """Verify that a watchlist belongs to a specific user."""
        try:
            stmt = (
                select(Watchlist)
                .where(Watchlist.id == watchlist_id, Watchlist.user_id == user_id)
                .options(lazyload(Watchlist.items))
            )
            watchlist = self._db.execute(stmt).scalar_one_or_none()
            return watchlist is not None
        except SQLAlchemyError as e:
            logger.error(f"Error verifying watchlist ownership: {e}")
            raise

    def get_all_watchlists(self, user_id: int) -> list[Watchlist]:
        """Get all watchlists for a specific user (lightweight)."""
        stmt = (
            select(Watchlist)
            .where(Watchlist.user_id == user_id)
            .options(lazyload(Watchlist.items))
        )
        return self._db.execute(stmt).scalars().all()

    def get_watchlist_with_relations(
        self, watchlist_id: int, user_id: int
    ) -> Watchlist | None:
        """Get a watchlist by its ID, loading related items with pre-loaded company data."""
        watchlist = (
            self._db.query(Watchlist)
            .filter_by(id=watchlist_id, user_id=user_id)
            .first()
        )

        if not watchlist:
            return None

        # Store items in a local variable to avoid re-accessing the relationship
        items = list(watchlist.items)  # ✅ Materialize once here

        if items:
            # Pre-load all company data (prices, metrics, ratios) in bulk
            profile_map = self.load_company_profiles_for_items(items)

            # Inject pre-loaded data into each item (no more DB queries!)
            for item in items:
                target = profile_map.get(item.symbol)
                if target:
                    item.set_company_profile(target)

        return watchlist

    def get_watchlist_item_with_relations(
        self, watchlist_id: int, watchlist_item_id: int, user_id: int
    ) -> WatchlistItem | None:
        """Get a watchlist item by its ID, ensuring it belongs to a user's watchlist, with pre-loaded company data."""
        # Join to verify ownership
        logging.info(
            f"Fetching watchlist item {watchlist_item_id} for watchlist {watchlist_id} and user {user_id}"
        )
        item = (
            self._db.query(WatchlistItem)
            .filter(
                WatchlistItem.id == watchlist_item_id,
                WatchlistItem.watchlist_id == watchlist_id,
            )
            .first()
        )

        if not item:
            return None

        # Pre-load company profile for this item
        profile_map = self.load_company_profiles_for_items([item])
        target = profile_map.get(item.symbol)
        if target:
            item.set_company_profile(target)

        return item

    def create_watchlist(self, watchlist_in: WatchlistCreate) -> Watchlist:
        """Create a new watchlist."""
        watchlist = Watchlist(**watchlist_in.model_dump(exclude_unset=True))
        self._db.add(watchlist)
        self._db.commit()
        self._db.refresh(watchlist)
        logger.info(f"Created watchlist {watchlist.id} for user {watchlist.user_id}")
        return watchlist

    def update_watchlist(
        self, watchlist_in: WatchlistUpdate, user_id: int
    ) -> Watchlist | None:
        """Create or update a watchlist."""
        watchlist = (
            self._db.query(Watchlist)
            .filter_by(id=watchlist_in.id, user_id=user_id)
            .first()
        )

        if not watchlist:
            logger.warning(f"Watchlist {watchlist_in.id} not found for user {user_id}")
            return None

        map_model(watchlist_in, watchlist)

        self._db.commit()
        self._db.refresh(watchlist)
        logger.info(f"Updated watchlist {watchlist.id}")
        return watchlist

    def delete_watchlist(self, watchlist_id: int, user_id: int) -> bool:
        """Delete a watchlist, ensuring it belongs to the user."""
        watchlist = (
            self._db.query(Watchlist)
            .filter_by(id=watchlist_id, user_id=user_id)
            .first()
        )

        if not watchlist:
            logger.warning(f"Watchlist {watchlist_id} not found for user {user_id}")
            return False

        self._db.delete(watchlist)
        self._db.commit()
        logger.info(f"Deleted watchlist {watchlist_id}")
        return True

    def load_company_profiles_for_items(
        self, items: list[WatchlistItem]
    ) -> dict[str, dict | None]:
        """
        Bulk load company profiles for all items with latest metrics, ratios, and prices.

        Returns plain dictionaries (not ORM objects) to avoid triggering lazy-loaded relationships.
        Includes:
        - Key metrics (latest per company per period)
        - Financial ratios (latest per company per period)
        - Stock prices (latest per company)

        Priority for metrics/ratios: FY > Q4 > Q3 > Q2 > Q1
        """
        from app.db.models.financial_statements import CompanyFinancialRatio

        if not items:
            return {}

        symbols = list({item.symbol for item in items})

        # Query companies - basic fields only
        stmt = select(Company).where(Company.symbol.in_(symbols))
        companies = self._db.execute(stmt).scalars().all()

        if not companies:
            return {symbol: None for symbol in symbols}

        company_ids = [c.id for c in companies]

        # Load latest financial ratios: 1 query for all companies
        all_ratios = (
            self._db.query(CompanyFinancialRatio)
            .filter(CompanyFinancialRatio.company_id.in_(company_ids))
            .all()
        )

        ratios_by_company = {}
        for company in companies:
            ratios_by_period = {}
            for ratio in all_ratios:
                if ratio.company_id == company.id:
                    period = ratio.period
                    if period not in ratios_by_period or (
                        ratio.fiscal_year > ratios_by_period[period].fiscal_year
                        or (
                            ratio.fiscal_year == ratios_by_period[period].fiscal_year
                            and ratio.date > ratios_by_period[period].date
                        )
                    ):
                        ratios_by_period[period] = ratio

            # Prefer FY > Q4 > Q3 > Q2 > Q1
            periods = ["FY", "Q4", "Q3", "Q2", "Q1"]
            for period in periods:
                if period in ratios_by_period:
                    ratio = ratios_by_period[period]
                    ratios_by_company[company.id] = {
                        "id": ratio.id,
                        "company_id": ratio.company_id,
                        "symbol": ratio.symbol,
                        "date": ratio.date,
                        "fiscal_year": ratio.fiscal_year,
                        "period": ratio.period,
                        "price_to_earnings_ratio": ratio.price_to_earnings_ratio,
                        "forward_price_to_earnings_growth_ratio": ratio.forward_price_to_earnings_growth_ratio,
                        "price_to_book_ratio": ratio.price_to_book_ratio,
                        "price_to_sales_ratio": ratio.price_to_sales_ratio,
                        "price_to_free_cash_flow_ratio": ratio.price_to_free_cash_flow_ratio,
                        "price_to_operating_cash_flow_ratio": ratio.price_to_operating_cash_flow_ratio,
                    }
                    break

        # Load latest stock prices: 1 query for all companies
        latest_prices = (
            self._db.query(CompanyStockPrice)
            .filter(CompanyStockPrice.company_id.in_(company_ids))
            .order_by(
                CompanyStockPrice.company_id,
                CompanyStockPrice.date.desc(),
            )
            .distinct(CompanyStockPrice.company_id)
            .all()
        )

        # Build result with plain dicts (no ORM objects)
        profiles = {}
        for company in companies:
            price_obj = next(
                (p for p in latest_prices if p.company_id == company.id), None
            )

            profiles[company.symbol] = {
                "id": company.id,
                "symbol": company.symbol,
                "company_name": company.company_name,
                "market_cap": company.market_cap,
                "currency": company.currency,
                "exchange": company.exchange,
                "industry": company.industry,
                "sector": company.sector,
                "image": company.image,
                "financial_ratios": [ratios_by_company[company.id]]
                if company.id in ratios_by_company
                else [],
                "stock_prices": [
                    {
                        "id": price_obj.id,
                        "company_id": price_obj.company_id,
                        "symbol": price_obj.symbol,
                        "date": price_obj.date,
                        "open_price": price_obj.open_price,
                        "close_price": price_obj.close_price,
                        "high_price": price_obj.high_price,
                        "low_price": price_obj.low_price,
                        "volume": price_obj.volume,
                        "change": price_obj.change,
                        "change_percent": price_obj.change_percent,
                    }
                ]
                if price_obj
                else [],
            }

        # Fill in missing symbols with None
        for symbol in symbols:
            if symbol not in profiles:
                profiles[symbol] = None

        return profiles

    def add_watchlist_item(
        self, watchlist_item_in: WatchlistItemCreate
    ) -> WatchlistItem:
        """Add an item to a watchlist."""
        item = WatchlistItem(**watchlist_item_in.model_dump(exclude_unset=True))
        self._db.add(item)
        self._db.commit()
        self._db.refresh(item)
        logger.info(f"Added {item.symbol} to watchlist {item.watchlist_id}")
        return item

    def delete_watchlist_item(
        self, watchlist_id: int, watchlist_item_id: int, user_id: int
    ) -> bool:
        """Delete a watchlist item, ensuring it belongs to a user's watchlist."""
        # Join to verify ownership
        item = (
            self._db.query(WatchlistItem)
            .join(Watchlist, WatchlistItem.watchlist_id == Watchlist.id)
            .filter(
                WatchlistItem.id == watchlist_item_id,
                Watchlist.id == watchlist_id,
                Watchlist.user_id == user_id,
            )
            .first()
        )

        if not item:
            logger.warning(
                f"Watchlist item {watchlist_item_id} not found or access denied"
            )
            return False

        self._db.delete(item)
        self._db.commit()
        logger.info(f"Deleted watchlist item {watchlist_item_id}")
        return True
