import logging

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.internal.market_data_sync_repo import (
    CompanyMarketDataSyncRepository,
)
from app.schemas.market_data import (
    CompanyGeneralNewsRead,
    CompanyGeneralNewsWrite,
    CompanyGradingNewsRead,
    CompanyGradingNewsWrite,
    CompanyGradingRead,
    CompanyGradingSummaryRead,
    CompanyGradingSummaryWrite,
    CompanyGradingWrite,
    CompanyPriceTargetNewsRead,
    CompanyPriceTargetNewsWrite,
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
    CompanyPriceTargetSummaryWrite,
    CompanyPriceTargetWrite,
    CompanyRatingSummaryRead,
    CompanyRatingSummaryWrite,
    CompanyStockNewsRead,
    CompanyStockNewsWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = logging.getLogger(__name__)


class CompanyMarketDataSyncService(BaseSyncService):
    """Service for syncing company financial health data from FMP API."""

    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        super().__init__(session)
        self._market_api_client = market_api_client
        self._repository = CompanyMarketDataSyncRepository(session)

    def upsert_gradings(self, symbol: str) -> list[CompanyGradingRead] | None:
        """
        Fetch and upsert company gradings.

        Args:
            symbol: Stock symbol

        Returns:
            List of upserted grading records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            grading_data = self._market_api_client.get_company_gradings(symbol)
            if not grading_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                grading_data, company.id, CompanyGradingWrite
            )
            gradings = self._repository.upsert_grading(symbol, records_to_persist)
            result = self._map_schema_list(gradings, CompanyGradingRead)

            logger.info(f"Successfully synced {len(result)} gradings for {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to sync gradings for {symbol}: {e}", exc_info=True)
            raise

    def upsert_grading_summary(self, symbol: str) -> CompanyGradingSummaryRead | None:
        """
        Fetch and upsert company grading summary.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted grading summary record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            summary_data = self._market_api_client.get_company_grading_summary(symbol)
            if not summary_data:
                return None

            summary_in = self._add_company_id_to_record(
                summary_data, company.id, CompanyGradingSummaryWrite
            )
            summary = self._repository.upsert_grading_summary(summary_in)
            result = self._map_schema_single(summary, CompanyGradingSummaryRead)

            logger.info(f"Successfully synced grading summary for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync grading summary for {symbol}: {e}", exc_info=True
            )
            raise

    def upsert_rating_summary(self, symbol: str) -> CompanyRatingSummaryRead | None:
        """
        Fetch and upsert rating summary for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted rating summary record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            rating_data = self._market_api_client.get_company_rating(symbol)
            if not rating_data:
                return None

            rating_in = self._add_company_id_to_record(
                rating_data, company.id, CompanyRatingSummaryWrite
            )
            rating = self._repository.upsert_rating_summary(rating_in)
            result = self._map_schema_single(rating, CompanyRatingSummaryRead)

            logger.info(f"Successfully synced rating summary for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync rating summary for {symbol}: {e}", exc_info=True
            )
            raise

    def upsert_price_target(self, symbol: str) -> CompanyPriceTargetRead | None:
        """
        Fetch and upsert price target for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted price target record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            price_target_data = self._market_api_client.get_price_target(symbol)
            if not price_target_data:
                return None

            price_target_in = self._add_company_id_to_record(
                price_target_data, company.id, CompanyPriceTargetWrite
            )
            price_target = self._repository.upsert_price_target(price_target_in)
            result = CompanyPriceTargetRead.model_validate(price_target)

            logger.info(f"Successfully synced price target for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync price target for {symbol}: {e}", exc_info=True
            )
            raise

    def upsert_price_target_summary(
        self, symbol: str
    ) -> CompanyPriceTargetSummaryRead | None:
        """
        Fetch and upsert price target summary for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted price target summary record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call
            price_target_summary_data = (
                self._market_api_client.get_price_target_summary(symbol)
            )
            if not price_target_summary_data:
                return None

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
            result = self._map_schema_single(
                price_target_summary, CompanyPriceTargetSummaryRead
            )

            logger.info(f"Successfully synced price target summary for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync price target summary for {symbol}: {e}", exc_info=True
            )
            raise

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
            if not api_data:
                return None

            # Map and validate write schemas
            news_in = self._add_company_id_to_records(
                api_data, None, CompanyGeneralNewsWrite
            )
            news = self._repository.upsert_general_news(news_in)
            result = self._map_schema_list(news, CompanyGeneralNewsRead)

            logger.info(f"Successfully synced {len(result)} general news articles")
            return result

        except Exception as e:
            logger.error(f"Failed to sync general news: {e}", exc_info=True)
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
            if not api_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyPriceTargetNewsWrite
            )
            news = self._repository.upsert_price_target_news(records_to_persist)
            result = self._map_schema_list(news, CompanyPriceTargetNewsRead)

            logger.info(
                f"Successfully synced {len(result)} price target news articles for {symbol}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync price target news for {symbol}: {e}", exc_info=True
            )
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
            if not api_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyGradingNewsWrite
            )
            news = self._repository.upsert_grading_news(records_to_persist)
            result = self._map_schema_list(news, CompanyGradingNewsRead)

            logger.info(
                f"Successfully synced {len(result)} grading news articles for {symbol}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync grading news for {symbol}: {e}", exc_info=True
            )
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
            if not api_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyStockNewsWrite
            )
            news = self._repository.upsert_stock_news(records_to_persist)
            result = self._map_schema_list(news, CompanyStockNewsRead)

            logger.info(
                f"Successfully synced {len(result)} stock news articles for {symbol}"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to sync stock news for {symbol}: {e}", exc_info=True)
            raise
