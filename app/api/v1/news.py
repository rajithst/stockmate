from fastapi import APIRouter, Depends

from app.dependencies.db import get_db_session
from app.schemas.market_data import NewsRead
from app.services.news_service import NewsService


router = APIRouter(prefix="")


def get_news_service(
    session=Depends(get_db_session),
) -> NewsService:
    return NewsService(session=session)


@router.get(
    "/latest", response_model=list[NewsRead], summary="Get latest news articles"
)
def get_latest_news(
    service: NewsService = Depends(get_news_service),
):
    """
    Retrieve the latest news articles.

    Returns:
        list[NewsArticleRead]: List of latest news articles
    """
    return service.get_latest_news()


@router.get(
    "/stock/{symbol}",
    response_model=list[NewsRead],
    summary="Get stock-specific news articles",
)
def get_stock_news(
    symbol: str,
    from_date: str,
    to_date: str,
    limit: int = 100,
    service: NewsService = Depends(get_news_service),
):
    """
    Retrieve stock-specific news articles for a given symbol within a date range.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        from_date: Start date in 'YYYY-MM-DD' format
        to_date: End date in 'YYYY-MM-DD' format
        limit: Number of records to fetch (default is 100)
        service: NewsService instance (injected)
    """
    return service.get_stock_news(
        symbol=symbol,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
    )
