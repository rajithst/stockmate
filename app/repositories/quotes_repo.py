import logging
from sqlalchemy.orm import Session

from app.db.models.quote import CompanyStockPrice, CompanyStockPriceChange
from app.schemas.quote import StockPriceChangeWrite, StockPriceWrite
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class QuotesRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def upsert_price_change(
        self, price_change: StockPriceChangeWrite
    ) -> CompanyStockPriceChange:
        """Upsert price change record by symbol."""
        return self._upsert_single(
            price_change,
            CompanyStockPriceChange,
            lambda pc: {"symbol": pc.symbol},
            "upsert_price_change",
        )

    def upsert_daily_price(
        self, daily_price: list[StockPriceWrite]
    ) -> CompanyStockPrice:
        """Upsert daily price records by symbol and date."""
        return self._upsert_single(
            daily_price,
            CompanyStockPrice,
            lambda dp: {"symbol": dp.symbol, "date": dp.date},
            "upsert_daily_price",
        )
