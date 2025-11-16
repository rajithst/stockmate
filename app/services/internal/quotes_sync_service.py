from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.internal.quote_sync_repo import CompanyQuoteSyncRepository
from app.schemas.quote import (
    CompanyDividendRead,
    CompanyDividendWrite,
    CompanyStockPeerRead,
    CompanyStockPeerWrite,
    CompanyStockSplitRead,
    CompanyStockSplitWrite,
    StockPriceChangeRead,
    StockPriceChangeWrite,
    StockPriceRead,
    StockPriceWrite,
)
from app.services.internal.base_sync_service import BaseSyncService
from datetime import datetime, timedelta

logger = getLogger(__name__)


class QuotesSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(session)
        self._market_api_client = market_api_client
        self._repository = CompanyQuoteSyncRepository(session)
        self._company_repository = CompanyRepository(session)

    def upsert_historical_prices(self, symbol, from_date, to_date):
        """
        Fetch and upsert historical stock prices for a company.

        Args:
            symbol: Stock symbol
            from_date: Start date for historical data
            to_date: End date for historical data
        Returns:
            List of upserted historical price records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            historical_data = self._market_api_client.get_historical_prices(
                symbol, from_date, to_date
            )
            if not historical_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                historical_data, company.id, StockPriceWrite
            )

            historical_prices = self._repository.upsert_historical_prices(
                records_to_persist
            )
            result = self._map_schema_list(historical_prices, StockPriceRead)

            logger.info(f"Upserted historical prices for symbol {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to upsert historical prices for symbol {symbol}: {e}")
            raise

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
            if not price_change_data:
                return None

            price_change_in = self._add_company_id_to_record(
                price_change_data, company.id, StockPriceChangeWrite
            )

            price_change = self._repository.upsert_price_change(price_change_in)
            result = self._map_schema_single(price_change, StockPriceChangeRead)

            logger.info(f"Upserted price change for symbol {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to upsert price change for symbol {symbol}: {e}")
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
            if not api_data:
                return None

            records_to_persist = self._add_company_id_to_record(
                api_data, company.id, StockPriceWrite
            )

            daily_price = self._repository.upsert_daily_price(records_to_persist)
            result = self._map_schema_single(daily_price, StockPriceRead)
            logger.info(f"Upserted daily price for symbol {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to upsert daily price for symbol {symbol}: {e}")
            raise

    def upsert_after_hours_prices(self, symbol) -> StockPriceRead | None:
        """
        Fetch and upsert after-hours stock price for a company.
        Args:
            symbol: Stock symbol
        Returns:
            Upserted after-hours price record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            api_data = self._market_api_client.get_after_hours_price(symbol)
            if not api_data:
                logger.warning(
                    f"No after-hours price data found from API for symbol {symbol}"
                )
                return None

            # Fetch the current daily price record to update after-hours price
            daily_price_record = self._repository.get_latest_daily_price_by_symbol(
                symbol
            )
            if not daily_price_record:
                logger.warning(
                    f"No daily price record found for symbol {symbol} to update after-hours price."
                )
                return None

            after_market_price = api_data.after_hours_price
            stock_price_write = StockPriceWrite.model_validate(
                {
                    **daily_price_record.to_dict(),
                    "after_hours_price": after_market_price,
                }
            )

            updated_record = self._repository.upsert_daily_price(stock_price_write)
            result = self._map_schema_single(updated_record, StockPriceRead)

            logger.info(f"Upserted after-hours price for symbol {symbol}")
            return result
        except Exception as e:
            logger.error(f"Failed to upsert after-hours price for symbol {symbol}: {e}")
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
            if not stock_splits_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                stock_splits_data, company.id, CompanyStockSplitWrite
            )
            splits = self._repository.upsert_stock_splits(records_to_persist)
            result = self._map_schema_list(splits, CompanyStockSplitRead)

            logger.info(f"Upserted stock splits for symbol {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to upsert stock splits for symbol {symbol}: {e}")
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
            if not peers_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                peers_data, company.id, CompanyStockPeerWrite
            )
            peers = self._repository.upsert_stock_peers(records_to_persist)
            result = self._map_schema_list(peers, CompanyStockPeerRead)

            logger.info(f"Upserted stock peers for symbol {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to upsert stock peers for symbol {symbol}: {e}")
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
            if not dividends_data:
                return None
            # add currency field to dividends_data
            for record in dividends_data:
                record.currency = company.currency
            records_to_persist = self._add_company_id_to_records(
                dividends_data, company.id, CompanyDividendWrite
            )
            dividends = self._repository.upsert_dividends(records_to_persist)
            result = self._map_schema_list(dividends, CompanyDividendRead)

            logger.info(f"Upserted dividends for symbol {symbol}")
            return result

        except Exception as e:
            logger.error(f"Error upserting dividends: {str(e)}", exc_info=True)
            raise

    def upsert_dividend_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[CompanyDividendRead] | None:
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
            all_symbols_with_currency = self._company_repository.get_all_companies()

            records_to_persist = []
            for company in all_symbols_with_currency:
                sym = company.symbol
                currency = company.currency
                sym_dividends = [
                    record for record in dividends_data if record.symbol == sym
                ]
                logger.info(
                    f"Found {len(sym_dividends)} dividend records to upsert for symbol: {sym}"
                )
                # Add currency to each dividend record
                records_to_persist.extend(
                    CompanyDividendWrite.model_validate(
                        {**record.model_dump(), "currency": currency}
                    )
                    for record in sym_dividends
                )

            dividends = self._repository.upsert_dividends(records_to_persist)
            result = self._map_schema_list(dividends, CompanyDividendRead)

            logger.info(
                f"Successfully upserted {len(result)} dividend records for {len(all_symbols_with_currency)} companies"
            )
            return result

        except Exception as e:
            logger.error(f"Error upserting dividend calendar: {str(e)}", exc_info=True)
            raise
