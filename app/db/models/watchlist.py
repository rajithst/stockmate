from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from app.db.models.company_metrics import CompanyKeyMetrics
from app.db.models.financial_statements import CompanyFinancialRatio

if TYPE_CHECKING:
    from app.db.models.company import Company
    from app.db.models.user import User

logger = getLogger(__name__)


class Watchlist(Base):
    __tablename__ = "watchlists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
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
    user: Mapped["User"] = relationship(
        "User", back_populates="watchlists", foreign_keys=[user_id], lazy="select"
    )
    items: Mapped[list["WatchlistItem"]] = relationship(
        "WatchlistItem",
        back_populates="watchlist",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def item_count(self) -> int:
        """Get the number of items in this watchlist."""
        return len(self.items)

    @property
    def symbols(self) -> list[str]:
        """Get all symbols in this watchlist."""
        return [item.symbol for item in self.items]

    def __repr__(self):
        return f"<Watchlist(name={self.name}, user_id={self.user_id}, items={self.item_count})>"


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"
    __table_args__ = (
        UniqueConstraint("watchlist_id", "symbol", name="uq_watchlist_item"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey("watchlists.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(12), index=True, nullable=False)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    watchlist: Mapped["Watchlist"] = relationship(
        "Watchlist", back_populates="items", foreign_keys=[watchlist_id], lazy="select"
    )

    def set_company_profile(self, company: "Any") -> None:
        """Set the company profile (pre-loaded to avoid N+1 queries)."""
        self._company_profile = company
        # Extract price from pre-loaded stock_prices list (avoid triggering DB query)
        self._current_price = (
            company.stock_prices[0].close_price if company.stock_prices else 0.0
        )
        self._price_change = company.stock_prices[0].change if company.stock_prices else 0.0
        self._price_change_percent = company.stock_prices[0].change_percent if company.stock_prices else 0.0
        # Extract latest metrics and ratios from pre-loaded lists
        self._key_metrics = company.key_metrics[0] if company.key_metrics else None
        self._financial_ratios = company.financial_ratios[0] if company.financial_ratios else None

    def _get_company_profile(self) -> "Company | None":
        """Fetch company profile from database."""
        # Return pre-loaded profile if available
        if hasattr(self, "_company_profile"):
            logger.info(f"Using pre-loaded company profile for {self.symbol}")
            return self._company_profile

        logger.info(
            f"cannot fetch company profile for {self.symbol} from cache - pre load data to avoid n+1 queries"
        )
        return None

    def _get_latest_financial_ratios(self) -> "CompanyFinancialRatio | None":
        """Fetch latest financial ratios for this symbol using repository logic."""
        # Return pre-loaded ratios if available
        if hasattr(self, "_financial_ratios"):
            logger.info(f"Using pre-loaded financial ratios for {self.symbol}")
            return self._financial_ratios

        logger.info(
            f"cannot fetch financial ratios for {self.symbol} from cache - pre load data to avoid n+1 queries"
        )
        return None

    def _get_key_metrics(self) -> "CompanyKeyMetrics | None":
        """Fetch latest key metrics for this symbol using repository logic."""
        # Return pre-loaded key metrics if available
        if hasattr(self, "_key_metrics"):
            logger.info(f"Using pre-loaded key metrics for {self.symbol}")
            return self._key_metrics

        logger.info(
            f"cannot fetch key metrics for {self.symbol} from cache - pre load data to avoid n+1 queries"
        )
        return None

    def _get_current_price(self) -> float:
        """Fetch the latest stock price from the database."""
        # Return pre-loaded price if available
        if hasattr(self, "_current_price"):
            logger.info(f"Using pre-loaded current price for {self.symbol}")
            return self._current_price

        logger.info(
            f"cannot fetch current price for {self.symbol} from cache - pre load data to avoid n+1 queries"
        )
        return 0.0

    def _get_price_change(self) -> float:
        """Fetch the latest price change from the database."""
        # Return pre-loaded price change if available
        if hasattr(self, "_price_change"):
            logger.info(f"Using pre-loaded price change for {self.symbol}")
            return self._price_change

        logger.info(
            f"cannot fetch price change for {self.symbol} from cache - pre load data to avoid n+1 queries"
        )
        return 0.0
    
    def _get_price_change_percent(self) -> float:
        """Fetch the latest price change percent from the database."""
        # Return pre-loaded price change percent if available
        if hasattr(self, "_price_change_percent"):
            logger.info(f"Using pre-loaded price change percent for {self.symbol}")
            return self._price_change_percent

        logger.info(
            f"cannot fetch price change percent for {self.symbol} from cache - pre load data to avoid n+1 queries"
        )
        return 0.0

    @property
    def company_profile(self) -> "Company | None":
        """Get the company profile for this watchlist item."""
        return self._get_company_profile()

    @property
    def financial_ratios(self) -> "CompanyFinancialRatio | None":
        """Get the latest financial ratios for this watchlist item."""
        return self._get_latest_financial_ratios()

    @property
    def key_metrics(self) -> "CompanyKeyMetrics | None":
        """Get the latest key metrics for this watchlist item."""
        return self._get_key_metrics()

    @property
    def current_price(self) -> float:
        """Get the current price for this symbol."""
        return self._get_current_price()
    
    @property
    def price_change(self) -> float:
        """Get the latest price change for this symbol."""
        return self._get_price_change()

    @property
    def price_change_percent(self) -> float:
        """Get the latest price change percent for this symbol."""
        return self._get_price_change_percent()

    def __repr__(self):
        return (
            f"<WatchlistItem(symbol={self.symbol}, watchlist_id={self.watchlist_id})>"
        )
