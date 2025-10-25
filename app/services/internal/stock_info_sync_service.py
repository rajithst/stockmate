from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.stock_info_repo import StockInfoRepository
from app.schemas.dividend import CompanyDividendRead, CompanyDividendWrite
from app.schemas.stock import (
    CompanyStockPeerRead,
    CompanyStockPeerWrite,
    CompanyStockSplitRead,
    CompanyStockSplitWrite,
)

logger = getLogger(__name__)


class StockInfoSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = StockInfoRepository(session)
        self._company_repository = CompanyRepository(session)

    def upsert_dividends(
        self, symbol: str, limit: int
    ) -> list[CompanyDividendRead] | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None
            dividends_data = self._market_api_client.get_dividends(symbol)
            if not dividends_data:
                logger.warning(f"No dividends found for symbol: {symbol}")
                return None
            dividends_in = [
                CompanyDividendWrite.model_validate(
                    {**dividend.model_dump(), "company_id": company.id}
                )
                for dividend in dividends_data
            ]
            dividends = self._repository.upsert_dividends(dividends_in)
            return [
                CompanyDividendRead.model_validate(dividend) for dividend in dividends
            ]
        except Exception as e:
            logger.error(f"Error fetching company for symbol {symbol}: {e}")
            return None

    def upsert_stock_splits(
        self, symbol: str, limit: int
    ) -> list[CompanyStockSplitRead] | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None
            stock_splits_data = self._market_api_client.get_stock_splits(symbol)
            if not stock_splits_data:
                logger.warning(f"No stock splits found for symbol: {symbol}")
                return None
            stock_splits_in = [
                CompanyStockSplitWrite.model_validate(
                    {**stock_split.model_dump(), "company_id": company.id}
                )
                for stock_split in stock_splits_data
            ]
            splits = self._repository.upsert_stock_splits(stock_splits_in)
            return [CompanyStockSplitRead.model_validate(split) for split in splits]
        except Exception as e:
            logger.error(f"Error upserting stock splits for symbol {symbol}: {e}")
            return None

    def upsert_stock_peers(self, symbol: str) -> list[CompanyStockPeerRead] | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None
            peers_data = self._market_api_client.get_stock_peer_companies(symbol)
            if not peers_data:
                logger.warning(f"No stock peers found for symbol: {symbol}")
                return None
            peers_in = [
                CompanyStockPeerWrite.model_validate(
                    {
                        **pd.model_dump(),
                        "company_id": company.id,
                    }
                )
                for pd in peers_data
            ]
            peers = self._repository.upsert_stock_peers(peers_in)
            return [CompanyStockPeerRead.model_validate(peer) for peer in peers]
        except Exception as e:
            logger.error(f"Error upserting stock peers for symbol {symbol}: {e}")
            return None
