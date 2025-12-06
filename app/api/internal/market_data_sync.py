from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.market_data import (
    CompanyGradingRead,
    CompanyGradingSummaryRead,
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
    CompanyRatingSummaryRead,
    NewsRead,
)
from app.services.internal.market_data_sync_service import CompanyMarketDataSyncService

router = APIRouter(prefix="")

get_market_data_sync_service = create_sync_service_provider(
    CompanyMarketDataSyncService
)


@router.get(
    "/gradings/{symbol}/sync",
    response_model=list[CompanyGradingRead],
    summary="Sync company gradings from external API",
    description="Fetches and upserts a company's grading data from the external API into the database.",
)
def sync_gradings(
    symbol: str,
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync a company's grading data from the external API and store it in the database."""
    grading = service.upsert_gradings(symbol)
    if not grading:
        raise HTTPException(
            status_code=404,
            detail="Gradings not found for symbol: {}".format(symbol),
        )
    return grading


@router.get(
    "/gradings/{symbol}/summary/sync",
    response_model=CompanyGradingSummaryRead,
    summary="Sync company grading summary from external API",
    description="Fetches and upserts a company's grading summary data from the external API into the database.",
)
def sync_grading_summary(
    symbol: str,
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync a company's grading summary from the external API and store it in the database."""
    grading_summary = service.upsert_grading_summary(symbol)
    if not grading_summary:
        raise HTTPException(
            status_code=404,
            detail="Grading summary not found for symbol: {}".format(symbol),
        )
    return grading_summary


@router.get(
    "/ratings/{symbol}/sync",
    response_model=CompanyRatingSummaryRead,
    summary="Sync company rating summary from external API",
    description="Fetches and upserts a company's rating summary from the external API into the database.",
)
def sync_rating_summary(
    symbol: str,
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync a company's rating summary from the external API and store it in the database."""
    rating_summary = service.upsert_rating_summary(symbol)
    if not rating_summary:
        raise HTTPException(
            status_code=404,
            detail="Rating summary not found for symbol: {}".format(symbol),
        )
    return rating_summary


@router.get(
    "/price-targets/{symbol}/sync",
    response_model=CompanyPriceTargetRead,
    summary="Sync company price target from external API",
    description="Fetches and upserts company's current price target from the external API into the database.",
)
def sync_price_target(
    symbol: str,
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync company's current price target from the external API and store in the database."""
    price_target = service.upsert_price_target(symbol)
    if not price_target:
        raise HTTPException(
            status_code=404,
            detail="Price target not found for symbol: {}".format(symbol),
        )
    return price_target


@router.get(
    "/price-targets/{symbol}/summary/sync",
    response_model=CompanyPriceTargetSummaryRead,
    summary="Sync company price target summary from external API",
    description="Fetches and upserts company's price target summary from the external API into the database.",
)
def sync_price_target_summary(
    symbol: str,
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync company's price target summary from the external API and store in the database."""
    summary = service.upsert_price_target_summary(symbol)
    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Price target summary not found for symbol: {}".format(symbol),
        )
    return summary


@router.get(
    "/stock-news/{symbol}/sync",
    response_model=list[NewsRead],
    summary="Sync company stock news from external API",
    description="Fetches and upserts company's stock news from the external API into the database.",
)
def sync_stock_news(
    symbol: str,
    from_date: str = Query(
        default=None,
        description="Start date for fetching news in YYYY-MM-DD format. If not provided, defaults to 30 days ago.",
    ),
    to_date: str = Query(
        default=None,
        description="End date for fetching news in YYYY-MM-DD format. If not provided, defaults to today.",
    ),
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync company stock news from the external API and store in the database."""
    news = service.upsert_stock_news(symbol, from_date, to_date, limit=100)
    if not news:
        raise HTTPException(
            status_code=404,
            detail="Stock news not found for symbol: {}".format(symbol),
        )
    return news


@router.get(
    "/general-news/sync",
    response_model=list[NewsRead],
    summary="Sync general market news from external API",
    description="Fetches and upserts general market news from the external API into the database.",
)
def sync_general_news(
    from_date: str,
    to_date: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync general market news from the external API and store in the database."""
    news = service.upsert_general_news(from_date, to_date, limit)
    if not news:
        raise HTTPException(
            status_code=404,
            detail="General market news not found for the given date range.",
        )
    return news


@router.get(
    "/stock-news/sync",
    response_model=list[NewsRead],
    summary="Sync stock news from external API",
    description="Fetches and upserts stock news from the external API into the database.",
)
def sync_latest_stock_news(
    from_date: str,
    to_date: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    service: CompanyMarketDataSyncService = Depends(get_market_data_sync_service),
):
    """Sync general market news from the external API and store in the database."""
    news = service.upsert_latest_stock_news(from_date, to_date, limit)
    if not news:
        raise HTTPException(
            status_code=404,
            detail="General market news not found for the given date range.",
        )
    return news
