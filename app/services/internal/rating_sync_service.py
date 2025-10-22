from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.rating_repo import CompanyRatingRepository
from app.schemas.rating import CompanyRatingSummaryRead, CompanyRatingSummaryWrite


class RatingSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = CompanyRatingRepository(session)

    def get_rating_summary(self, symbol: str) -> list[CompanyRatingSummaryRead]:
        ratings = self._repository.get_rating_summary_by_symbol(symbol)
        return [
            CompanyRatingSummaryRead.model_validate(rating.model_dump())
            for rating in ratings
        ]

    def upsert_rating_summary(self, symbol: str) -> CompanyRatingSummaryRead | None:
        rating_data = self._market_api_client.get_company_ratings(symbol)
        if not rating_data:
            return None
        rating_in = CompanyRatingSummaryWrite.model_validate(rating_data.model_dump())
        rating = self._repository.upsert_rating_summary(rating_in)
        return CompanyRatingSummaryRead.model_validate(rating.model_dump())
