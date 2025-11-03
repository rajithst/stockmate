import logging
from sqlalchemy.orm import Session

from app.db.models.quote import StockPrice, StockPriceChange
from app.schemas.quote import StockPriceChangeWrite, StockPriceWrite
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class QuotesRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def upsert_price_change(
        self, price_change: StockPriceChangeWrite
    ) -> StockPriceChange:
        """Upsert price change record by symbol."""
        return self._upsert_single(
            price_change,
            StockPriceChange,
            lambda pc: {"symbol": pc.symbol},
            "upsert_price_change",
        )

    def upsert_daily_price(self, daily_price: list[StockPriceWrite]) -> StockPrice:
        """Upsert daily price records by symbol and date."""
        return self._upsert_single(
            daily_price,
            StockPrice,
            lambda dp: {"symbol": dp.symbol, "date": dp.date},
            "upsert_daily_price",
        )
