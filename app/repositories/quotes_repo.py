from sqlalchemy.orm import Session

from app.db.models.quote import StockPriceChange
from app.schemas.quote import StockPriceChangeWrite
from app.util.model_mapper import map_model


class QuotesRepository:
    def __init__(self, session: Session):
        self._db = session

    def upsert_price_change(
        self, price_change: StockPriceChangeWrite
    ) -> StockPriceChange | None:
        existing = (
            self._db.query(StockPriceChange)
            .filter_by(symbol=price_change.symbol)
            .first()
        )
        if existing:
            record = map_model(existing, price_change)
        else:
            record = StockPriceChange(**price_change.model_dump(exclude_unset=True))
            self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record
