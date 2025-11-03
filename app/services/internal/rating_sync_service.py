from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.rating_repo import CompanyRatingRepository
from app.schemas.rating import CompanyRatingSummaryRead, CompanyRatingSummaryWrite
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class RatingSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = CompanyRatingRepository(session)

    def get_rating_summary(self, symbol: str) -> list[CompanyRatingSummaryRead]:
        """Get cached rating summary for a symbol."""
        ratings = self._repository.get_rating_summary_by_symbol(symbol)
        return self._map_schema_list(ratings, CompanyRatingSummaryRead)

    def upsert_rating_summary(self, symbol: str) -> CompanyRatingSummaryRead | None:
        """
        Fetch and upsert rating summary for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted rating summary record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            rating_data = self._market_api_client.get_company_rating(symbol)
            if not self._validate_api_response(rating_data, "rating_summary", symbol):
                return None

            rating_in = self._add_company_id_to_record(
                rating_data, company.id, CompanyRatingSummaryWrite
            )
            rating = self._repository.upsert_rating_summary(rating_in)
            result = self._map_schema_single(rating, CompanyRatingSummaryRead)

            self._log_sync_success("rating_summary", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("rating_summary", symbol, e)
            raise
