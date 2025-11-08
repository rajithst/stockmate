from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.price_target_repo import CompanyPriceTargetRepository
from app.schemas.market_data import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
    CompanyPriceTargetSummaryWrite,
    CompanyPriceTargetWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class PriceTargetSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = CompanyPriceTargetRepository(session)

    def get_price_targets(self, symbol: str) -> list[CompanyPriceTargetRead]:
        """Get cached price targets for a symbol."""
        price_targets = self._repository.get_price_targets_by_symbol(symbol)
        return self._map_schema_list(price_targets, CompanyPriceTargetRead)

    def upsert_price_target(self, symbol: str) -> CompanyPriceTargetRead | None:
        """
        Fetch and upsert price target for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted price target record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            price_target_data = self._market_api_client.get_price_target(symbol)
            if not self._validate_api_response(
                price_target_data, "price_target", symbol
            ):
                return None

            price_target_in = self._add_company_id_to_record(
                price_target_data, company.id, CompanyPriceTargetWrite
            )
            price_target = self._repository.upsert_price_target(price_target_in)
            result = CompanyPriceTargetRead.model_validate(price_target)

            self._log_sync_success("price_target", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("price_target", symbol, e)
            raise

    def upsert_price_target_summary(
        self, symbol: str
    ) -> CompanyPriceTargetSummaryRead | None:
        """
        Fetch and upsert price target summary for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted price target summary record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            price_target_summary_data = (
                self._market_api_client.get_price_target_summary(symbol)
            )
            if not self._validate_api_response(
                price_target_summary_data, "price_target_summary", symbol
            ):
                return None

            price_target_summary_in = CompanyPriceTargetSummaryWrite.model_validate(
                {
                    **price_target_summary_data.model_dump(),
                    "company_id": company.id,
                    "publishers": ", ".join(price_target_summary_data.publishers)
                    if price_target_summary_data.publishers
                    else None,
                }
            )
            price_target_summary = self._repository.upsert_price_target_summary(
                price_target_summary_in
            )
            result = self._map_schema_single(
                price_target_summary, CompanyPriceTargetSummaryRead
            )

            self._log_sync_success("price_target_summary", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("price_target_summary", symbol, e)
            raise
