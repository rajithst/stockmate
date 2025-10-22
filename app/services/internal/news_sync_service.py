from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.news_repo import CompanyNewsRepository
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGeneralNewsWrite,
    CompanyGradingNewsRead,
    CompanyGradingNewsWrite,
    CompanyPriceTargetNewsRead,
    CompanyPriceTargetNewsWrite,
)


class NewsSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = CompanyNewsRepository(session)

    def get_general_news(self, symbol: str) -> list[CompanyGeneralNewsRead]:
        news = self._repository.get_general_news_by_symbol(symbol)
        return [CompanyGeneralNewsRead.model_validate(n.model_dump()) for n in news]

    def get_price_target_news(self, symbol: str) -> list[CompanyPriceTargetNewsRead]:
        news = self._repository.get_price_target_news_by_symbol(symbol)
        return [CompanyPriceTargetNewsRead.model_validate(n.model_dump()) for n in news]

    def get_grading_news(self, symbol: str) -> list[CompanyGradingNewsRead]:
        news = self._repository.get_grading_news_by_symbol(symbol)
        return [CompanyGradingNewsRead.model_validate(n.model_dump()) for n in news]

    def upsert_general_news(self, symbol: str) -> list[CompanyGeneralNewsRead] | None:
        news_data = self._market_api_client.get_company_general_news(symbol)
        if not news_data:
            return None
        news_in = [
            CompanyGeneralNewsWrite.model_validate(news.model_dump())
            for news in news_data
        ]
        news = self._repository.upsert_general_news(news_in)
        return [CompanyGeneralNewsRead.model_validate(n.model_dump()) for n in news]

    def upsert_price_target_news(
        self, symbol: str
    ) -> list[CompanyPriceTargetNewsRead] | None:
        news_data = self._market_api_client.get_company_price_target_news(symbol)
        if not news_data:
            return None
        news_in = [
            CompanyPriceTargetNewsWrite.model_validate(news.model_dump())
            for news in news_data
        ]
        news = self._repository.upsert_price_target_news(news_in)
        return [CompanyPriceTargetNewsRead.model_validate(n.model_dump()) for n in news]

    def upsert_grading_news(self, symbol: str) -> list[CompanyGradingNewsRead] | None:
        news_data = self._market_api_client.get_company_grading_news(symbol)
        if not news_data:
            return None
        news_in = [
            CompanyGradingNewsWrite.model_validate(news.model_dump())
            for news in news_data
        ]
        news = self._repository.upsert_grading_news(news_in)
        return [CompanyGradingNewsRead.model_validate(n.model_dump()) for n in news]
