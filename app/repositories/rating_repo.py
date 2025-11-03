import logging
from sqlalchemy.orm import Session

from app.db.models.ratings import CompanyRatingSummary
from app.schemas.rating import CompanyRatingSummaryWrite
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class CompanyRatingRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_rating_summary_by_symbol(self, symbol: str) -> list[CompanyRatingSummary]:
        """Get all rating summaries for a symbol."""
        return self._get_by_filter(CompanyRatingSummary, {"symbol": symbol})

    def upsert_rating_summary(
        self, rating: CompanyRatingSummaryWrite
    ) -> CompanyRatingSummary:
        """Upsert rating summary by symbol."""
        return self._upsert_single(
            rating,
            CompanyRatingSummary,
            lambda r: {"symbol": r.symbol},
            "upsert_rating_summary",
        )
