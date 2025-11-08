from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.metrics_repo import MetricsRepository
from app.schemas.financial_statements import (
    CompanyFinancialRatioRead,
    CompanyFinancialRatioWrite,
)
from app.schemas.financial_health import (
    CompanyFinancialScoresRead,
    CompanyFinancialScoresWrite,
)
from app.schemas.company_metrics import CompanyKeyMetricsRead, CompanyKeyMetricsWrite
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class MetricsSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = MetricsRepository(session)

    def get_key_metrics(self, symbol: str) -> list[CompanyKeyMetricsRead]:
        """Get cached key metrics for a symbol."""
        key_metrics = self._repository.get_key_metrics_by_symbol(symbol)
        return self._map_schema_list(key_metrics, CompanyKeyMetricsRead)

    def get_financial_ratios(self, symbol: str) -> list[CompanyFinancialRatioRead]:
        """Get cached financial ratios for a symbol."""
        financial_ratios = self._repository.get_financial_ratios_by_symbol(symbol)
        return self._map_schema_list(financial_ratios, CompanyFinancialRatioRead)

    def get_financial_scores(self, symbol: str) -> list[CompanyFinancialScoresRead]:
        """Get cached financial scores for a symbol."""
        financial_scores = self._repository.get_financial_scores_by_symbol(symbol)
        return self._map_schema_list(financial_scores, CompanyFinancialScoresRead)

    def upsert_key_metrics(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyKeyMetricsRead] | None:
        """
        Fetch and upsert key metrics for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted key metrics records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            key_metrics_data = self._market_api_client.get_key_metrics(
                symbol, period=period, limit=limit
            )
            if not self._validate_api_response(key_metrics_data, "key_metrics", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                key_metrics_data, company.id, CompanyKeyMetricsWrite
            )
            key_metrics = self._repository.upsert_key_metrics(records_to_persist)
            result = self._map_schema_list(key_metrics, CompanyKeyMetricsRead)

            self._log_sync_success("key_metrics", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("key_metrics", symbol, e)
            raise

    def upsert_financial_ratios(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyFinancialRatioRead] | None:
        """
        Fetch and upsert financial ratios for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted financial ratio records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            financial_ratios_data = self._market_api_client.get_financial_ratios(
                symbol, period=period, limit=limit
            )
            if not self._validate_api_response(
                financial_ratios_data, "financial_ratios", symbol
            ):
                return None

            records_to_persist = self._add_company_id_to_records(
                financial_ratios_data, company.id, CompanyFinancialRatioWrite
            )
            financial_ratios = self._repository.upsert_financial_ratios(
                records_to_persist
            )
            result = self._map_schema_list(financial_ratios, CompanyFinancialRatioRead)

            self._log_sync_success("financial_ratios", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("financial_ratios", symbol, e)
            raise

    def upsert_financial_scores(self, symbol: str) -> CompanyFinancialScoresRead | None:
        """
        Fetch and upsert financial scores for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted financial scores record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            financial_scores_data = self._market_api_client.get_financial_scores(symbol)
            if not self._validate_api_response(
                financial_scores_data, "financial_scores", symbol
            ):
                return None

            financial_scores_in = self._add_company_id_to_record(
                financial_scores_data, company.id, CompanyFinancialScoresWrite
            )
            financial_scores = self._repository.upsert_financial_scores(
                financial_scores_in
            )
            result = self._map_schema_single(
                financial_scores, CompanyFinancialScoresRead
            )

            self._log_sync_success("financial_scores", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("financial_scores", symbol, e)
            raise
