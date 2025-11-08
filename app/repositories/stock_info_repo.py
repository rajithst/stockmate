import logging
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.company import Company
from app.db.models.dividend import CompanyDividend
from app.db.models.stock import CompanyStockPeer, CompanyStockSplit
from app.schemas.quote import CompanyDividendWrite
from app.schemas.quote import CompanyStockPeerWrite, CompanyStockSplitWrite
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class StockInfoRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all_company_symbols_with_currency(self) -> dict[str, str]:
        """Retrieve all company stock symbols with their currency."""
        statement = select(Company.symbol, Company.currency)
        results = self._db.execute(statement).all()
        return {symbol: currency for symbol, currency in results}

    def get_dividends_by_symbol(self, symbol: str) -> list[CompanyDividend]:
        """Get all dividends for a symbol."""
        return self._get_by_filter(CompanyDividend, {"symbol": symbol})

    def get_stock_splits_by_symbol(self, symbol: str) -> list[CompanyStockSplit]:
        """Get all stock splits for a symbol."""
        return self._get_by_filter(CompanyStockSplit, {"symbol": symbol})

    def get_stock_peers_by_symbol(self, symbol: str) -> list[CompanyStockPeer]:
        """Get all stock peers for a symbol."""
        return self._get_by_filter(CompanyStockPeer, {"symbol": symbol})

    def upsert_dividends(
        self, dividends_data: list[CompanyDividendWrite]
    ) -> list[CompanyDividend]:
        """Upsert multiple dividend records."""
        return self._upsert_records(
            dividends_data,
            CompanyDividend,
            lambda div: {"symbol": div.symbol, "date": div.date},
            "upsert_dividends",
        )

    def upsert_stock_splits(
        self, splits_data: list[CompanyStockSplitWrite]
    ) -> list[CompanyStockSplit]:
        """Upsert multiple stock split records."""
        return self._upsert_records(
            splits_data,
            CompanyStockSplit,
            lambda split: {"symbol": split.symbol, "date": split.date},
            "upsert_stock_splits",
        )

    def upsert_stock_peers(
        self, peers_data: list[CompanyStockPeerWrite]
    ) -> list[CompanyStockPeer]:
        """Upsert multiple stock peer records."""
        return self._upsert_records(
            peers_data,
            CompanyStockPeer,
            lambda peer: {"symbol": peer.symbol, "company_id": peer.company_id},
            "upsert_stock_peers",
        )
