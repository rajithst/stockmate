from logging import getLogger
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.news_repo import CompanyNewsRepository
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGeneralNewsWrite,
    CompanyGradingNewsRead,
    CompanyGradingNewsWrite,
    CompanyPriceTargetNewsRead,
    CompanyPriceTargetNewsWrite,
    CompanyStockNewsRead,
    CompanyStockNewsWrite,
)

logger = getLogger(__name__)


class NewsSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = CompanyNewsRepository(session)
        self._company_repository = CompanyRepository(session)

    def get_general_news(self, symbol: str) -> list[CompanyGeneralNewsRead]:
        news = self._repository.get_general_news_by_symbol(symbol)
        return [CompanyGeneralNewsRead.model_validate(n.model_dump()) for n in news]

    def get_price_target_news(self, symbol: str) -> list[CompanyPriceTargetNewsRead]:
        news = self._repository.get_price_target_news_by_symbol(symbol)
        return [CompanyPriceTargetNewsRead.model_validate(n.model_dump()) for n in news]

    def get_grading_news(self, symbol: str) -> list[CompanyGradingNewsRead]:
        news = self._repository.get_grading_news_by_symbol(symbol)
        return [CompanyGradingNewsRead.model_validate(n.model_dump()) for n in news]

    def upsert_general_news(
        self, from_date: str, to_date: str, limit: int = 100
    ) -> list[CompanyGeneralNewsRead] | None:
        try:
            news_data = self._market_api_client.get_latest_general_news(
                from_date, to_date, limit
            )
            print(news_data)
            if not news_data:
                logger.info("No general news data found from external API.")
                return None
            news_in = [
                CompanyGeneralNewsWrite.model_validate(**news.model_dump())
                for news in news_data
            ]
            print(news_in)
            news = self._repository.upsert_general_news(news_in)
            return [CompanyGeneralNewsRead.model_validate(n) for n in news]
        except Exception as e:
            logger.error(f"Error upserting general news: {e}")
            return None

    def upsert_price_target_news(
        self, symbol: str, limit: int = 100
    ) -> list[CompanyPriceTargetNewsRead] | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(
                    f"Company with symbol {symbol} not found in the database."
                )
                return None

            news_data = self._market_api_client.get_price_target_news(symbol)
            if not news_data:
                logger.info(
                    f"No price target news data found for symbol {symbol} from external API."
                )
                return None
            news_in = [
                CompanyPriceTargetNewsWrite.model_validate(
                    {
                        **news.model_dump(),
                        "company_id": company.id,
                    }
                )
                for news in news_data
            ]
            news = self._repository.upsert_price_target_news(news_in)
            return [
                CompanyPriceTargetNewsRead.model_validate(n.model_dump()) for n in news
            ]
        except Exception as e:
            logger.error(f"Error upserting price target news for symbol {symbol}: {e}")
            return None

    def upsert_grading_news(
        self, symbol: str, limit: int = 100
    ) -> list[CompanyGradingNewsRead] | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(
                    f"Company with symbol {symbol} not found in the database."
                )
                return None

            news_data = self._market_api_client.get_grading_news(symbol)
            if not news_data:
                logger.info(
                    f"No grading news data found for symbol {symbol} from external API."
                )
                return None
            news_in = [
                CompanyGradingNewsWrite.model_validate(
                    {
                        **news.model_dump(),
                        "company_id": company.id,
                    }
                )
                for news in news_data
            ]
            news = self._repository.upsert_grading_news(news_in)
            return [CompanyGradingNewsRead.model_validate(n.model_dump()) for n in news]
        except Exception as e:
            logger.error(f"Error upserting grading news for symbol {symbol}: {e}")
            return None

    def upsert_stock_news(self, symbol: str) -> list[CompanyGeneralNewsRead] | None:
        try:
            company = self._repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(
                    f"Company with symbol {symbol} not found in the database."
                )
                return None

            news_data = self._market_api_client.get_stock_news(symbol)
            if not news_data:
                logger.info(
                    f"No stock news data found for symbol {symbol} from external API."
                )
                return None
            news_in = [
                CompanyStockNewsWrite.model_validate(
                    {**news.model_dump(), "company_id": company.id}
                )
                for news in news_data
            ]
            news = self._repository.upsert_stock_news(news_in)
            return [CompanyStockNewsRead.model_validate(n.model_dump()) for n in news]
        except Exception as e:
            logger.error(f"Error upserting stock news for symbol {symbol}: {e}")
            return None
