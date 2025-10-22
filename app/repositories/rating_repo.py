from sqlalchemy.orm import Session

from app.db.models.ratings import CompanyRatingSummary
from app.schemas.rating import CompanyRatingSummaryRead, CompanyRatingSummaryWrite
from app.util import map_model


class CompanyRatingRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_rating_summary_by_symbol(self, symbol: str) -> list[CompanyRatingSummary]:
        return (
            self._db.query(CompanyRatingSummaryRead)
            .filter(CompanyRatingSummaryRead.symbol == symbol)
            .all()
        )

    def upsert_rating_summary(
        self, ratings: CompanyRatingSummaryWrite
    ) -> CompanyRatingSummary:
        existing = (
            self._db.query(CompanyRatingSummaryRead)
            .filter_by(symbol=ratings.symbol)
            .first()
        )
        if existing:
            record = map_model(existing, ratings)
        else:
            record = CompanyRatingSummaryRead(**ratings.model_dump(exclude_unset=True))
            self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record
