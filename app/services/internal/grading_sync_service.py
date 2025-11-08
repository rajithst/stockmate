from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.grading_repo import GradingRepository, GradingSummaryRepository
from app.schemas.market_data import (
    CompanyGradingRead,
    CompanyGradingSummaryRead,
    CompanyGradingSummaryWrite,
    CompanyGradingWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class GradingSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._grading_repository = GradingRepository(session)
        self._grading_summary_repository = GradingSummaryRepository(session)

    def upsert_gradings(self, symbol: str) -> list[CompanyGradingRead] | None:
        """
        Fetch and upsert company gradings.

        Args:
            symbol: Stock symbol

        Returns:
            List of upserted grading records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            grading_data = self._market_api_client.get_company_gradings(symbol)
            if not self._validate_api_response(grading_data, "gradings", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                grading_data, company.id, CompanyGradingWrite
            )
            gradings = self._grading_repository.upsert_grading(
                symbol, records_to_persist
            )
            result = self._map_schema_list(gradings, CompanyGradingRead)

            self._log_sync_success("gradings", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("gradings", symbol, e)
            raise

    def upsert_grading_summary(self, symbol: str) -> CompanyGradingSummaryRead | None:
        """
        Fetch and upsert company grading summary.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted grading summary record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            summary_data = self._market_api_client.get_company_grading_summary(symbol)
            if not self._validate_api_response(summary_data, "grading_summary", symbol):
                return None

            summary_in = self._add_company_id_to_record(
                summary_data, company.id, CompanyGradingSummaryWrite
            )
            summary = self._grading_summary_repository.upsert_grading_summary(
                summary_in
            )
            result = self._map_schema_single(summary, CompanyGradingSummaryRead)

            self._log_sync_success("grading_summary", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("grading_summary", symbol, e)
            raise
