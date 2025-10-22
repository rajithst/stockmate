from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.price_target_repo import CompanyPriceTargetRepository
from app.schemas.price_target import CompanyPriceTargetRead, CompanyPriceTargetWrite


class PriceTargetSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = CompanyPriceTargetRepository(session)

    def get_price_targets(self, symbol: str) -> list[CompanyPriceTargetRead]:
        price_targets = self._repository.get_price_targets_by_symbol(symbol)
        return [
            CompanyPriceTargetRead.model_validate(pt.model_dump())
            for pt in price_targets
        ]

    def upsert_price_targets(self, symbol: str) -> list[CompanyPriceTargetRead] | None:
        price_target_data = self._market_api_client.get_company_price_targets(symbol)
        if not price_target_data:
            return None
        price_targets_in = [
            CompanyPriceTargetWrite.model_validate(pt.model_dump())
            for pt in price_target_data
        ]
        price_targets = self._repository.upsert_price_targets(price_targets_in)
        return [
            CompanyPriceTargetRead.model_validate(pt.model_dump())
            for pt in price_targets
        ]
