from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.news_repo import CompanyNewsRepository
from app.schemas.market_data import (
    CompanyGeneralNewsRead,
    CompanyGeneralNewsWrite,
    CompanyGradingNewsRead,
    CompanyGradingNewsWrite,
    CompanyPriceTargetNewsRead,
    CompanyPriceTargetNewsWrite,
    CompanyStockNewsRead,
    CompanyStockNewsWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class NewsSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = CompanyNewsRepository(session)

    def get_general_news(self, symbol: str) -> list[CompanyGeneralNewsRead]:
        """Get cached general news for a symbol."""
        news = self._repository.get_general_news_by_symbol(symbol)
        return self._map_schema_list(news, CompanyGeneralNewsRead)

    def get_price_target_news(self, symbol: str) -> list[CompanyPriceTargetNewsRead]:
        """Get cached price target news for a symbol."""
        news = self._repository.get_price_target_news_by_symbol(symbol)
        return self._map_schema_list(news, CompanyPriceTargetNewsRead)

    def get_grading_news(self, symbol: str) -> list[CompanyGradingNewsRead]:
        """Get cached grading news for a symbol."""
        news = self._repository.get_grading_news_by_symbol(symbol)
        return self._map_schema_list(news, CompanyGradingNewsRead)

    def upsert_general_news(
        self, from_date: str, to_date: str, limit: int = 100
    ) -> list[CompanyGeneralNewsRead] | None:
        """
        Fetch and upsert general market news.

        Args:
            from_date: Start date for news
            to_date: End date for news
            limit: Number of records to fetch

        Returns:
            List of upserted general news records or None if not found
        """
        try:
            # General news doesn't require company lookup
            api_data = self._market_api_client.get_latest_general_news(
                from_date, to_date, limit
            )
            if not self._validate_api_response(api_data, "general_news", "market"):
                return None

            # Map and validate write schemas
            news_in = self._add_company_id_to_records(
                api_data, None, CompanyGeneralNewsWrite
            )
            news = self._repository.upsert_general_news(news_in)
            result = self._map_schema_list(news, CompanyGeneralNewsRead)

            self._log_sync_success("general_news", len(result), "market")
            return result

        except Exception as e:
            self._log_sync_failure("general_news", "market", e)
            raise

    def upsert_price_target_news(
        self, symbol: str, limit: int = 100
    ) -> list[CompanyPriceTargetNewsRead] | None:
        """
        Fetch and upsert price target news for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch

        Returns:
            List of upserted price target news records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            api_data = self._market_api_client.get_price_target_news(symbol)
            if not self._validate_api_response(api_data, "price_target_news", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyPriceTargetNewsWrite
            )
            news = self._repository.upsert_price_target_news(records_to_persist)
            result = self._map_schema_list(news, CompanyPriceTargetNewsRead)

            self._log_sync_success("price_target_news", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("price_target_news", symbol, e)
            raise

    def upsert_grading_news(
        self, symbol: str, limit: int = 100
    ) -> list[CompanyGradingNewsRead] | None:
        """
        Fetch and upsert grading news for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch

        Returns:
            List of upserted grading news records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            api_data = self._market_api_client.get_grading_news(symbol)
            if not self._validate_api_response(api_data, "grading_news", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyGradingNewsWrite
            )
            news = self._repository.upsert_grading_news(records_to_persist)
            result = self._map_schema_list(news, CompanyGradingNewsRead)

            self._log_sync_success("grading_news", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("grading_news", symbol, e)
            raise

    def upsert_stock_news(
        self, symbol: str, limit: int = 100
    ) -> list[CompanyStockNewsRead] | None:
        """
        Fetch and upsert stock news for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch

        Returns:
            List of upserted stock news records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            api_data = self._market_api_client.get_stock_news(symbol)
            if not self._validate_api_response(api_data, "stock_news", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyStockNewsWrite
            )
            news = self._repository.upsert_stock_news(records_to_persist)
            result = self._map_schema_list(news, CompanyStockNewsRead)

            self._log_sync_success("stock_news", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("stock_news", symbol, e)
            raise
