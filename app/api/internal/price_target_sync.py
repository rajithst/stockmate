from fastapi import APIRouter, Depends, HTTPException

from app.api.internal.config import ERROR_MESSAGES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.price_target import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.services.internal.price_target_sync_service import PriceTargetSyncService

router = APIRouter(prefix="", tags=[TAGS["price_target"]["name"]])

# Create dependency provider for PriceTargetSyncService
get_price_target_sync_service = create_sync_service_provider(PriceTargetSyncService)


@router.get(
    "/{symbol}/sync",
    response_model=CompanyPriceTargetRead,
    summary="Sync company price target from external API",
    description="Fetches and upserts company's current price target from the external API into the database.",
)
def sync_price_target(
    symbol: str,
    service: PriceTargetSyncService = Depends(get_price_target_sync_service),
):
    """Sync company's current price target from the external API and store in the database."""
    price_target = service.upsert_price_target(symbol)
    if not price_target:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_PRICE_TARGETS"].format(symbol=symbol),
        )
    return price_target


@router.get(
    "/{symbol}/summary/sync",
    response_model=CompanyPriceTargetSummaryRead,
    summary="Sync company price target summary from external API",
    description="Fetches and upserts company's price target summary from the external API into the database.",
)
def sync_price_target_summary(
    symbol: str,
    service: PriceTargetSyncService = Depends(get_price_target_sync_service),
):
    """Sync company's price target summary from the external API and store in the database."""
    summary = service.upsert_price_target_summary(symbol)
    if not summary:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_PRICE_TARGET_SUMMARY"].format(
                symbol=symbol
            ),
        )
    return summary
