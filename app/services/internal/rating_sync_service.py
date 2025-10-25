from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.rating_repo import CompanyRatingRepository
from app.schemas.rating import CompanyRatingSummaryRead, CompanyRatingSummaryWrite

logger = getLogger(__name__)


class RatingSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = CompanyRatingRepository(session)
        self._company_repository = CompanyRepository(session)

    def get_rating_summary(self, symbol: str) -> list[CompanyRatingSummaryRead]:
        ratings = self._repository.get_rating_summary_by_symbol(symbol)
        return [
            CompanyRatingSummaryRead.model_validate(rating.model_dump())
            for rating in ratings
        ]

    def upsert_rating_summary(self, symbol: str) -> CompanyRatingSummaryRead | None:
        try:
            # Fetch rating data from external API client
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            rating_data = self._market_api_client.get_company_rating(symbol)
            if not rating_data:
                logger.warning(f"No rating data found for symbol: {symbol}")
                return None
            rating_in = CompanyRatingSummaryWrite.model_validate(
                {**rating_data.model_dump(), "company_id": company.id}
            )
            rating = self._repository.upsert_rating_summary(rating_in)
            return CompanyRatingSummaryRead.model_validate(rating)
        except Exception as e:
            logger.error(f"Error upserting ratings for symbol {symbol}: {e}")
            return None
