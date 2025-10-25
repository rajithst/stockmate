from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.price_target_repo import CompanyPriceTargetRepository
from app.schemas.price_target import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
    CompanyPriceTargetSummaryWrite,
    CompanyPriceTargetWrite,
)

logger = getLogger(__name__)


class PriceTargetSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = CompanyPriceTargetRepository(session)
        self._company_repository = CompanyRepository(session)

    def get_price_targets(self, symbol: str) -> list[CompanyPriceTargetRead]:
        price_targets = self._repository.get_price_targets_by_symbol(symbol)
        return [
            CompanyPriceTargetRead.model_validate(pt.model_dump())
            for pt in price_targets
        ]

    def upsert_price_target(self, symbol: str) -> CompanyPriceTargetRead | None:
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            # Fetch price target data from external API client
            price_target_data = self._market_api_client.get_price_target(symbol)
            if not price_target_data:
                logger.warning(f"No price target data found for symbol: {symbol}")
                return None
            logger.info(price_target_data)
            price_target_in = CompanyPriceTargetWrite.model_validate(
                {**price_target_data.model_dump(), "company_id": company.id}
            )
            price_target = self._repository.upsert_price_target(price_target_in)
            return CompanyPriceTargetRead.model_validate(price_target)
        except Exception as e:
            logger.error(f"Error upserting price targets for symbol {symbol}: {e}")
            return None

    def upsert_price_target_summary(
        self, symbol: str
    ) -> CompanyPriceTargetSummaryRead | None:
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            # Fetch price target summary data from external API client
            price_target_summary_data = (
                self._market_api_client.get_price_target_summary(symbol)
            )
            if not price_target_summary_data:
                logger.warning(
                    f"No price target summary data found for symbol: {symbol}"
                )
                return None
            logger.info(price_target_summary_data)
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
            return CompanyPriceTargetSummaryRead.model_validate(price_target_summary)
        except Exception as e:
            logger.error(
                f"Error upserting price target summary for symbol {symbol}: {e}"
            )
            return None
