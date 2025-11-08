"""Revenue product segmentation sync service for fetching and storing segmentation data."""

import logging

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.db.models.company import Company
from app.repositories.revenue_product_segmentation_repo import (
    CompanyRevenueProductSegmentationRepository,
)
from app.schemas.company_metrics import (
    CompanyRevenueProductSegmentationRead,
    CompanyRevenueProductSegmentationWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = logging.getLogger(__name__)


class RevenueProductSegmentationSyncService(BaseSyncService):
    """Service for syncing revenue product segmentation data from FMP to database."""

    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = CompanyRevenueProductSegmentationRepository(session)

    def _get_company_by_symbol(self, symbol: str) -> Company | None:
        """Get company by symbol from database."""
        company = self._session.query(Company).filter(Company.symbol == symbol).first()
        return company

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
            if not self._validate_api_response(
                fmp_segmentations, "revenue_product_segmentation", symbol
            ):
                logger.warning(f"Invalid API response for {symbol}")
                return None

            segmentations = self._add_company_id_to_records(
                fmp_segmentations, company.id, CompanyRevenueProductSegmentationWrite
            )

            results = self._repository.upsert_revenue_segmentations(segmentations)
            mapped_results = self._map_schema_list(
                results, CompanyRevenueProductSegmentationRead
            )
            self._log_sync_success("revenue_product_segmentation", len(results), symbol)
            return mapped_results
        except Exception as e:
            self._log_sync_failure("revenue_product_segmentation", symbol, e)
            raise
