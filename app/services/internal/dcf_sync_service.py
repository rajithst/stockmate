from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.dcf_repo import DiscountedCashFlowRepository
from app.schemas.dcf import DiscountedCashFlowRead, DiscountedCashFlowWrite

logger = getLogger(__name__)


class DiscountedCashFlowSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        self._market_api_client = market_api_client
        self._repository = DiscountedCashFlowRepository(session)
        self._company_repository = CompanyRepository(session)

    def upsert_discounted_cash_flow(self, symbol: str) -> DiscountedCashFlowRead | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            dcf_data = self._market_api_client.get_discounted_cash_flow(symbol)
            if not dcf_data:
                logger.warning(
                    f"No discounted cash flow data found for symbol: {symbol}"
                )
                return None

            logger.info(dcf_data)

            dcf_in = DiscountedCashFlowWrite.model_validate(
                {**dcf_data.model_dump(), "company_id": company.id}
            )
            dcf = self._repository.upsert_discounted_cash_flow(dcf_in)
            return DiscountedCashFlowRead.model_validate(dcf)
        except Exception as e:
            logger.error(
                f"Error upserting discounted cash flow for symbol {symbol}: {e}"
            )
            return None
