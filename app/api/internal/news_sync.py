from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.internal.config import DEFAULTS, ERROR_MESSAGES, LIMITS, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
    CompanyStockNewsRead,
)
from app.services.internal.news_sync_service import NewsSyncService

router = APIRouter(prefix="", tags=[TAGS["news"]["name"]])

# Create dependency provider for NewsSyncService
get_news_sync_service = create_sync_service_provider(NewsSyncService)


@router.get(
    "/stock/{symbol}/sync",
    response_model=list[CompanyStockNewsRead],
    summary="Sync company stock news from external API",
    description="Fetches and upserts company's stock news from the external API into the database.",
)
def sync_stock_news(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["news_limit"],
        ge=LIMITS["news_limit"]["min"],
        le=LIMITS["news_limit"]["max"],
    ),
    service: NewsSyncService = Depends(get_news_sync_service),
):
    """Sync company stock news from the external API and store in the database."""
    news = service.upsert_stock_news(symbol, limit)
    if not news:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_STOCK_NEWS"].format(symbol=symbol),
        )
    return news


@router.get(
    "/general/sync",
    response_model=list[CompanyGeneralNewsRead],
    summary="Sync general market news from external API",
    description="Fetches and upserts general market news from the external API into the database.",
)
def sync_general_news(
    from_date: str,
    to_date: str,
    limit: int = Query(
        default=DEFAULTS["general_news_limit"],
        ge=LIMITS["general_news_limit"]["min"],
        le=LIMITS["general_news_limit"]["max"],
    ),
    service: NewsSyncService = Depends(get_news_sync_service),
):
    """Sync general market news from the external API and store in the database."""
    news = service.upsert_general_news(from_date, to_date, limit)
    if not news:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_GENERAL_NEWS"],
        )
    return news


@router.get(
    "/price-target/{symbol}/sync",
    response_model=list[CompanyPriceTargetNewsRead],
    summary="Sync company price target news from external API",
    description="Fetches and upserts company's price target news from the external API into the database.",
)
def sync_price_target_news(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["news_limit"],
        ge=LIMITS["news_limit"]["min"],
        le=LIMITS["news_limit"]["max"],
    ),
    service: NewsSyncService = Depends(get_news_sync_service),
):
    """Sync company's price target news from the external API and store in the database."""
    news = service.upsert_price_target_news(symbol, limit)
    if not news:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_PRICE_TARGET_NEWS"].format(symbol=symbol),
        )
    return news


@router.get(
    "/grading/{symbol}/sync",
    response_model=list[CompanyGradingNewsRead],
    summary="Sync company grading news from external API",
    description="Fetches and upserts company's grading news from the external API into the database.",
)
def sync_grading_news(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["news_limit"],
        ge=LIMITS["news_limit"]["min"],
        le=LIMITS["news_limit"]["max"],
    ),
    service: NewsSyncService = Depends(get_news_sync_service),
):
    """Sync company's grading news from the external API and store in the database."""
    news = service.upsert_grading_news(symbol, limit)
    if not news:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_GRADING_NEWS"].format(symbol=symbol),
        )
    return news
