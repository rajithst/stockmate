from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.price_target import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.services.internal.price_target_sync_service import PriceTargetSyncService

router = APIRouter(prefix="/price-target", tags=["Internal Price Target"])


def get_price_target_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> PriceTargetSyncService:
    """
    Provides PriceTargetSyncService with required dependencies.
    """
    return PriceTargetSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/{symbol}/sync",
    response_model=CompanyPriceTargetRead,
    summary="Sync company price target from external API",
    description="Fetches and upserts company's current price target from the external API into the database.",
)
async def sync_company_price_target(
    symbol: str,
    service: PriceTargetSyncService = Depends(get_price_target_sync_service),
):
    """
    Sync company's current price target from the external API and store in the database.
    """
    price_target = service.upsert_price_target(symbol)
    if not price_target:
        raise HTTPException(
            status_code=404, detail=f"Price target not found for symbol: {symbol}"
        )
    return price_target


@router.get(
    "/{symbol}/summary/sync",
    response_model=CompanyPriceTargetSummaryRead,
    summary="Sync company price target summary from external API",
    description="Fetches and upserts company's price target summary from the external API into the database.",
)
async def sync_company_price_target_summary(
    symbol: str,
    service: PriceTargetSyncService = Depends(get_price_target_sync_service),
):
    """
    Sync company's price target summary from the external API and store in the database.
    """
    summary = service.upsert_price_target_summary(symbol)
    if not summary:
        raise HTTPException(
            status_code=404,
            detail=f"Price target summary not found for symbol: {symbol}",
        )
    return summary
