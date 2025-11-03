from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.dcf_repo import DiscountedCashFlowRepository
from app.schemas.dcf import DiscountedCashFlowRead, DiscountedCashFlowWrite
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class DiscountedCashFlowSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        super().__init__(market_api_client, session)
        self._repository = DiscountedCashFlowRepository(session)

    def upsert_discounted_cash_flow(self, symbol: str) -> DiscountedCashFlowRead | None:
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
            if not self._validate_api_response(dcf_data, "dcf_valuation", symbol):
                return None

            dcf_in = self._add_company_id_to_record(
                dcf_data, company.id, DiscountedCashFlowWrite
            )
            dcf = self._repository.upsert_discounted_cash_flow(dcf_in)
            result = self._map_schema_single(dcf, DiscountedCashFlowRead)

            self._log_sync_success("dcf_valuation", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("dcf_valuation", symbol, e)
            raise
