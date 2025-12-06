from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.repositories.market_data_repo import (
    CompanyMarketDataRepository,
)
from app.schemas.market_data import NewsRead


class NewsService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self.market_data_repo = CompanyMarketDataRepository(session)

    def get_latest_news(self) -> list[NewsRead]:
        """Retrieve the latest news articles."""
        today = datetime.utcnow().date()
        one_month_ago = today - timedelta(days=30)
        today_str = today.isoformat()
        one_month_ago_str = one_month_ago.isoformat()
        latest_news = self.market_data_repo.get_latest_news(
            from_date=one_month_ago_str, to_date=today_str, limit=100
        )
        news_read_models = [NewsRead.model_validate(news) for news in latest_news]
        return news_read_models

    def get_stock_news(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        limit: int = 100,
    ) -> list[NewsRead]:
        """Retrieve stock-specific news articles for a given symbol within a date range."""
        if not from_date:
            from_date_dt = datetime.utcnow() - timedelta(days=30)
            from_date_str = from_date_dt.date().strftime("%Y-%m-%d")
        else:
            from_date_str = from_date
        if not to_date:
            to_date = datetime.utcnow()
            to_date_str = to_date.date().strftime("%Y-%m-%d")
        else:
            to_date_str = to_date

        stock_news = self.market_data_repo.get_stock_news(
            symbol=symbol,
            from_date=from_date_str,
            to_date=to_date_str,
            limit=limit,
        )
        news_read_models = [NewsRead.model_validate(news) for news in stock_news]
        return news_read_models
