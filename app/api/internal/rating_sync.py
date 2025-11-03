from fastapi import APIRouter, Depends, HTTPException

from app.api.internal.config import ERROR_MESSAGES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.rating import CompanyRatingSummaryRead
from app.services.internal.rating_sync_service import RatingSyncService

router = APIRouter(prefix="", tags=[TAGS["rating"]["name"]])

# Create dependency provider for RatingSyncService
get_rating_sync_service = create_sync_service_provider(RatingSyncService)


@router.get(
    "/{symbol}/sync",
    response_model=CompanyRatingSummaryRead,
    summary="Sync company rating summary from external API",
    description="Fetches and upserts a company's rating summary from the external API into the database.",
)
def sync_rating_summary(
    symbol: str, service: RatingSyncService = Depends(get_rating_sync_service)
):
    """Sync a company's rating summary from the external API and store it in the database."""
    rating_summary = service.upsert_rating_summary(symbol)
    if not rating_summary:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_RATING_SUMMARY"].format(symbol=symbol),
        )
    return rating_summary
