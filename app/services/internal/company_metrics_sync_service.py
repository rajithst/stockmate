import logging


from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.internal.company_metrics_sync_repo import (
    CompanyMetricsSyncRepository,
)
from app.schemas.company_metrics import (
    CompanyAnalystEstimateRead,
    CompanyAnalystEstimateWrite,
    CompanyDiscountedCashFlowRead,
    CompanyDiscountedCashFlowWrite,
    CompanyKeyMetricsWrite,
    CompanyRevenueProductSegmentationRead,
    CompanyRevenueProductSegmentationWrite,
)
from app.schemas.company_metrics import CompanyKeyMetricsRead
from app.services.internal.base_sync_service import BaseSyncService

logger = logging.getLogger(__name__)


class CompanyMetricsSyncService(BaseSyncService):
    """Service for syncing company metrics data from FMP API."""

    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        super().__init__(session)
        self._market_api_client = market_api_client
        self._session = session
        self._repository = CompanyMetricsSyncRepository(session)

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
            List of synced analyst estimate schemas or None on failure
        """
        try:
            # Get company
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Fetch from API
            api_data = self._market_api_client.get_analyst_estimates(
                symbol=symbol, period=period, limit=limit
            )
            if not api_data:
                logger.error(f"No data returned for analyst estimates of {symbol}")
                return None

            analyst_estimates_in = self._add_company_id_to_records(
                api_data, company.id, CompanyAnalystEstimateWrite
            )

            # Persist to database
            analyst_estimates = self._repository.upsert_analyst_estimates(
                analyst_estimates_in
            )

            # Map to read schema
            result = self._map_schema_list(
                analyst_estimates, CompanyAnalystEstimateRead
            )
            logger.info(
                f"Successfully synced {len(analyst_estimates)} analyst estimates for {symbol}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Error syncing analyst estimates for {symbol}: {str(e)}", exc_info=True
            )
            return None

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
            if not key_metrics_data:
                logger.error(f"No data returned for key metrics of {symbol}")
                return None

            records_to_persist = self._add_company_id_to_records(
                key_metrics_data, company.id, CompanyKeyMetricsWrite
            )
            key_metrics = self._repository.upsert_key_metrics(records_to_persist)
            result = self._map_schema_list(key_metrics, CompanyKeyMetricsRead)

            logger.info(f"Successfully synced {len(result)} key metrics for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Error syncing key metrics for {symbol}: {str(e)}", exc_info=True
            )
            return None

    def upsert_key_metrics_ttm(self, symbol: str) -> CompanyKeyMetricsRead | None:
        """
        Fetch and upsert trailing twelve months key metrics for a company.

        Args:
            symbol: Stock symbol
        Returns:
            Upserted key metrics record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            key_metrics_data = self._market_api_client.get_key_metrics_ttm(symbol)
            if not key_metrics_data:
                logger.error(f"No data returned for TTM key metrics of {symbol}")
                return None

            key_metrics_in = self._add_company_id_to_record(
                key_metrics_data, company.id, CompanyKeyMetricsWrite
            )
            key_metrics = self._repository.upsert_key_metrics([key_metrics_in])
            if not key_metrics:
                logger.error(f"Failed to upsert TTM key metrics for {symbol}")
                return None

            result = self._map_schema_single(key_metrics[0], CompanyKeyMetricsRead)

            logger.info(f"Successfully synced TTM key metrics for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Error syncing TTM key metrics for {symbol}: {str(e)}", exc_info=True
            )
            return None

    def upsert_discounted_cash_flow(
        self, symbol: str
    ) -> CompanyDiscountedCashFlowRead | None:
        """
        Fetch and upsert discounted cash flow valuation for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted DCF record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            dcf_data = self._market_api_client.get_discounted_cash_flow(symbol)
            if not dcf_data:
                logger.error(f"No data returned for DCF of {symbol}")
                return None

            dcf_in = self._add_company_id_to_record(
                dcf_data, company.id, CompanyDiscountedCashFlowWrite
            )
            dcf = self._repository.upsert_discounted_cash_flow(dcf_in)
            result = self._map_schema_single(dcf, CompanyDiscountedCashFlowRead)

            logger.info(f"Successfully synced DCF for {symbol}")
            return result

        except Exception as e:
            logger.error(f"Error syncing DCF for {symbol}: {str(e)}", exc_info=True)
            return None

    def upsert_revenue_segmentations(
        self,
        symbol: str,
        period: str = "annual",
    ) -> list[CompanyRevenueProductSegmentationRead] | None:
        """
        Sync revenue product segmentation for a single symbol.

        Args:
            symbol: The stock symbol to sync
            limit: Maximum number of records to fetch

        Returns:
            RevenueSegmentationSyncResult with sync status and counts
        """
        try:
            # Get company
            company = self._get_company_or_fail(symbol)
            if not company:
                return None
            fmp_segmentations = (
                self._market_api_client.get_revenue_product_segmentation(
                    symbol=symbol, period=period
                )
            )
            if not fmp_segmentations:
                logger.warning(
                    f"No data returned for revenue product segmentation of {symbol}"
                )
                return None

            segmentations = self._add_company_id_to_records(
                fmp_segmentations, company.id, CompanyRevenueProductSegmentationWrite
            )

            results = self._repository.upsert_revenue_segmentations(segmentations)
            mapped_results = self._map_schema_list(
                results, CompanyRevenueProductSegmentationRead
            )
            logger.info(
                f"Successfully synced {len(results)} revenue segmentations for {symbol}"
            )
            return mapped_results
        except Exception as e:
            logger.error(
                f"Error syncing revenue product segmentation for {symbol}: {str(e)}",
                exc_info=True,
            )
            return None
