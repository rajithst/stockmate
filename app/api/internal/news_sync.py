from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyPriceTargetNewsRead,
    CompanyGradingNewsRead,
)
from app.services.internal.news_sync_service import NewsSyncService

router = APIRouter(prefix="/news", tags=["Internal News"])


def get_news_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> NewsSyncService:
    """
    Provides NewsSyncService with required dependencies.
    """
    return NewsSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/general/{symbol}/sync",
    response_model=List[CompanyGeneralNewsRead],
    summary="Sync company general news from external API",
    description="Fetches and upserts company's general news from the external API into the database.",
)
async def sync_company_general_news(
    symbol: str,
    limit: int = Query(default=100, ge=1, le=1000),
    service: NewsSyncService = Depends(get_news_sync_service),
):
    """
    Sync company's general news from the external API and store in the database.
    """
    news = service.upsert_general_news(symbol, limit)
    if not news:
        raise HTTPException(
            status_code=404, detail=f"General news not found for symbol: {symbol}"
        )
    return news


@router.get(
    "/price-target/{symbol}/sync",
    response_model=List[CompanyPriceTargetNewsRead],
    summary="Sync company price target news from external API",
    description="Fetches and upserts company's price target news from the external API into the database.",
)
async def sync_company_price_target_news(
    symbol: str,
    limit: int = Query(default=100, ge=1, le=1000),
    service: NewsSyncService = Depends(get_news_sync_service),
):
    """
    Sync company's price target news from the external API and store in the database.
    """
    news = service.upsert_price_target_news(symbol, limit)
    if not news:
        raise HTTPException(
            status_code=404, detail=f"Price target news not found for symbol: {symbol}"
        )
    return news


@router.get(
    "/grading/{symbol}/sync",
    response_model=List[CompanyGradingNewsRead],
    summary="Sync company grading news from external API",
    description="Fetches and upserts company's grading news from the external API into the database.",
)
async def sync_company_grading_news(
    symbol: str,
    limit: int = Query(default=100, ge=1, le=1000),
    service: NewsSyncService = Depends(get_news_sync_service),
):
    """
    Sync company's grading news from the external API and store in the database.
    """
    news = service.upsert_grading_news(symbol, limit)
    if not news:
        raise HTTPException(
            status_code=404, detail=f"Grading news not found for symbol: {symbol}"
        )
    return news
