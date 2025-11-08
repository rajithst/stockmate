import logging

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.analyst_estimate_repo import CompanyAnalystEstimateRepository
from app.schemas.company_metrics import (
    CompanyAnalystEstimateRead,
    CompanyAnalystEstimateWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = logging.getLogger(__name__)


class AnalystEstimateSyncService(BaseSyncService):
    """Service for syncing analyst estimates from FMP to database."""

    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        super().__init__(market_api_client, session)
        self._repository = CompanyAnalystEstimateRepository(session)

    def upsert_analyst_estimates(
        self,
        symbol: str,
        period: str = "quarter",
        limit: int = 10,
    ) -> list[CompanyAnalystEstimateRead] | None:
        """
        Sync analyst estimates for a single symbol.

        Args:
            symbol: The stock symbol to sync
            period: The period for estimates ('quarter' or 'annual')
            limit: Maximum number of records to fetch

        Returns:
            AnalystEstimateSyncResult with sync status and counts
        """
        try:
            # Get company
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            api_data = self._market_api_client.get_analyst_estimates(
                symbol=symbol, period=period, limit=limit
            )
            if not self._validate_api_response(api_data, "analyst_estimates", symbol):
                return None

            analyst_estimates_in = self._add_company_id_to_records(
                api_data, company.id, CompanyAnalystEstimateWrite
            )
            analyst_estimates = self._repository.upsert_analyst_estimates(
                analyst_estimates_in
            )
            result = self._map_schema_list(
                analyst_estimates, CompanyAnalystEstimateRead
            )
            self._log_sync_success("analyst_estimates", len(analyst_estimates), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("analyst_estimates", symbol, e)
