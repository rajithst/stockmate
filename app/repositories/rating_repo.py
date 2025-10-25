from sqlalchemy.orm import Session

from app.db.models.ratings import CompanyRatingSummary
from app.schemas.rating import CompanyRatingSummaryWrite
from app.util.model_mapper import map_model


class CompanyRatingRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_rating_summary_by_symbol(self, symbol: str) -> list[CompanyRatingSummary]:
        return (
            self._db.query(CompanyRatingSummary)
            .filter(CompanyRatingSummary.symbol == symbol)
            .all()
        )

    def upsert_rating_summary(
        self, rating: CompanyRatingSummaryWrite
    ) -> CompanyRatingSummary:
        existing = (
            self._db.query(CompanyRatingSummary).filter_by(symbol=rating.symbol).first()
        )
        if existing:
            record = map_model(existing, rating)
        else:
            record = CompanyRatingSummary(**rating.model_dump(exclude_unset=True))
            self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record
