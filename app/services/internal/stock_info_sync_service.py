from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.stock_info_repo import StockInfoRepository
from app.schemas.dividend import CompanyDividendRead, CompanyDividendWrite
from app.schemas.stock import (
    CompanyStockPeerRead,
    CompanyStockSplitRead,
    CompanyStockSplitWrite,
)


class StockInfoSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = StockInfoRepository(session)

    def upsert_dividends(self, symbol: str) -> list[CompanyDividendRead] | None:
        dividends_data = self._market_api_client.get_dividends(symbol)
        if not dividends_data:
            return None
        dividends_in = [
            CompanyDividendWrite.model_validate(dividend.model_dump())
            for dividend in dividends_data
        ]
        dividends = self._repository.upsert_dividends(dividends_in)
        return [
            CompanyDividendWrite.model_validate(dividend.model_dump())
            for dividend in dividends
        ]

    def upsert_stock_splits(self, symbol: str) -> list[CompanyStockSplitRead] | None:
        stock_splits_data = self._market_api_client.get_stock_splits(symbol)
        if not stock_splits_data:
            return None
        stock_splits_in = [
            CompanyStockSplitWrite.model_validate(stock_split.model_dump())
            for stock_split in stock_splits_data
        ]
        splits = self._repository.upsert_stock_splits(stock_splits_in)
        return [
            CompanyStockSplitWrite.model_validate(split.model_dump())
            for split in splits
        ]

    def upsert_stock_peers(self, symbol: str) -> list[CompanyStockPeerRead] | None:
        peers_data = self._market_api_client.get_stock_peers(symbol)
        if not peers_data:
            return None
        peers = self._repository.upsert_stock_peers(symbol, peers_data)
        return [
            CompanyStockPeerRead.model_validate(peer.model_dump()) for peer in peers
        ]
