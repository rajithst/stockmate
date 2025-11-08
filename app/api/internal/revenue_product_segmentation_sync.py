from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.internal.config import ERROR_MESSAGES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.company_metrics import (
    CompanyRevenueProductSegmentationRead,
)
from app.services.internal.revenue_product_segmentation_sync_service import (
    RevenueProductSegmentationSyncService,
)

router = APIRouter(prefix="", tags=[TAGS["revenue_segmentation"]["name"]])

# Create dependency provider for RevenueProductSegmentationSyncService
get_revenue_segmentation_sync_service = create_sync_service_provider(
    RevenueProductSegmentationSyncService
)


@router.get(
    "/revenue-product-segmentation/{symbol}/sync",
    response_model=list[CompanyRevenueProductSegmentationRead] | None,
    summary="Sync revenue product segmentation from external API",
    description="Fetches and upserts revenue product segmentation data from the external API into the database.",
)
def sync_revenue_product_segmentation(
    symbol: str,
    period: str = Query(
        default="annual",
        description="The period for revenue segmentation ('annual' or 'quarter')",
    ),
    service: RevenueProductSegmentationSyncService = Depends(
        get_revenue_segmentation_sync_service
    ),
):
    """
    Sync revenue product segmentation from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        service: RevenueProductSegmentationSyncService instance (injected)

    Returns:
        RevenueSegmentationSyncResult: Sync result with created/updated counts

    Raises:
        HTTPException: 404 if revenue segmentation not found
    """
    result = service.upsert_revenue_segmentations(symbol, period)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES.get(
                "NOT_FOUND_REVENUE_SEGMENTATION",
                f"Revenue segmentation not found for {symbol}",
            ),
        )

    return result
