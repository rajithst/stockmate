from logging import getLogger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.stock_info_repo import StockInfoRepository
from app.schemas.quote import CompanyDividendRead, CompanyDividendWrite
from app.schemas.quote import (
    CompanyStockPeerRead,
    CompanyStockPeerWrite,
    CompanyStockSplitRead,
    CompanyStockSplitWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class StockInfoSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = StockInfoRepository(session)

    def upsert_dividend_calendar(self) -> list[CompanyDividendRead] | None:
        """
        Fetch and upsert dividends for a company.

        Returns:
            List of upserted dividend records or None if not found
        """
        try:
            from_date = datetime.now().strftime("%Y-%m-%d")
            to_date = (datetime.now().replace(day=1) + timedelta(days=90)).strftime(
                "%Y-%m-%d"
            )
            dividends_data = self._market_api_client.get_dividend_calendar(
                from_date, to_date
            )

            # get dividends from dividend data for all available companies in the db
            all_symbols = self._repository.get_all_company_symbols()

            records_to_persist = []
            for sym in all_symbols:
                sym_dividends = [
                    record for record in dividends_data if record.symbol == sym
                ]
                logger.info(
                    f"Found {len(sym_dividends)} dividend records to upsert for symbol: {sym}"
                )
                records_to_persist.extend(
                    CompanyDividendWrite.model_validate(record.model_dump())
                    for record in sym_dividends
                )

            dividends = self._repository.upsert_dividends(records_to_persist)
            result = self._map_schema_list(dividends, CompanyDividendRead)

            logger.info(
                f"Successfully upserted {len(result)} dividend records for {len(all_symbols)} companies"
            )
            return result

        except Exception as e:
            logger.error(f"Error upserting dividend calendar: {str(e)}", exc_info=True)
            raise

    def upsert_dividends(
        self, symbol: str, limit: int = 50
    ) -> list[CompanyDividendRead] | None:
        """
        Fetch and upsert dividends for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            dividends_data = self._market_api_client.get_dividends(symbol, limit)
            if not self._validate_api_response(dividends_data, "dividends", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                dividends_data, company.id, CompanyDividendWrite
            )
            dividends = self._repository.upsert_dividends(records_to_persist)
            result = self._map_schema_list(dividends, CompanyDividendRead)

            self._log_sync_success("dividends", len(result), symbol)
            return result

        except Exception as e:
            logger.error(f"Error upserting dividends: {str(e)}", exc_info=True)
            raise

    def upsert_stock_splits(
        self, symbol: str, limit: int = 50
    ) -> list[CompanyStockSplitRead] | None:
        """
        Fetch and upsert stock splits for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch

        Returns:
            List of upserted stock split records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            stock_splits_data = self._market_api_client.get_stock_splits(symbol)
            if not self._validate_api_response(
                stock_splits_data, "stock_splits", symbol
            ):
                return None

            records_to_persist = self._add_company_id_to_records(
                stock_splits_data, company.id, CompanyStockSplitWrite
            )
            splits = self._repository.upsert_stock_splits(records_to_persist)
            result = self._map_schema_list(splits, CompanyStockSplitRead)

            self._log_sync_success("stock_splits", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("stock_splits", symbol, e)
            raise

    def upsert_stock_peers(self, symbol: str) -> list[CompanyStockPeerRead] | None:
        """
        Fetch and upsert stock peers for a company.

        Args:
            symbol: Stock symbol

        Returns:
            List of upserted stock peer records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            peers_data = self._market_api_client.get_stock_peer_companies(symbol)
            if not self._validate_api_response(peers_data, "stock_peers", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                peers_data, company.id, CompanyStockPeerWrite
            )
            peers = self._repository.upsert_stock_peers(records_to_persist)
            result = self._map_schema_list(peers, CompanyStockPeerRead)

            self._log_sync_success("stock_peers", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("stock_peers", symbol, e)
            raise
