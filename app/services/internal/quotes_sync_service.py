from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.quotes_repo import QuotesRepository
from app.schemas.quote import (
    StockPriceChangeRead,
    StockPriceChangeWrite,
    StockPriceRead,
    StockPriceWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class QuotesSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = QuotesRepository(session)

    def upsert_price_change(self, symbol: str) -> StockPriceChangeRead | None:
        """
        Fetch and upsert stock price change/quote for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted price change record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            price_change_data = self._market_api_client.get_price_change_quote(symbol)
            if not self._validate_api_response(
                price_change_data, "price_change", symbol
            ):
                return None

            price_change_in = self._add_company_id_to_record(
                price_change_data, company.id, StockPriceChangeWrite
            )

            price_change = self._repository.upsert_price_change(price_change_in)
            result = self._map_schema_single(price_change, StockPriceChangeRead)

            self._log_sync_success("price_change", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("price_change", symbol, e)
            raise

    def upsert_daily_prices(self, symbol: str) -> StockPriceRead | None:
        """
        Fetch and upsert daily stock prices for a company.

        Args:
            symbol: Stock symbol
        Returns:
            Upserted daily prices records or None if not found
        """

        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            api_data = self._market_api_client.get_current_price_quote(symbol)
            if not self._validate_api_response(api_data, "daily_price", symbol):
                return None

            records_to_persist = self._add_company_id_to_record(
                api_data, company.id, StockPriceWrite
            )

            daily_price = self._repository.upsert_daily_price(records_to_persist)
            result = self._map_schema_single(daily_price, StockPriceRead)
            self._log_sync_success("daily_prices", 1, symbol)
            return result

        except Exception as e:
            self._log_sync_failure("daily_prices", symbol, e)
            raise
