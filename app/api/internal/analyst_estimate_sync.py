from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.internal.config import DEFAULTS, ERROR_MESSAGES, LIMITS, PERIOD_TYPES
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.company_metrics import (
    CompanyAnalystEstimateRead,
)
from app.services.internal.analyst_estimate_sync_service import (
    AnalystEstimateSyncService,
)

router = APIRouter(
    prefix="",
)

# Create dependency provider for AnalystEstimateSyncService
get_analyst_estimate_sync_service = create_sync_service_provider(
    AnalystEstimateSyncService
)


@router.post(
    "/analyst-estimates/{symbol}/sync",
    response_model=list[CompanyAnalystEstimateRead],
    summary="Sync analyst estimates from external API",
    description="Fetches and upserts analyst estimates from the external API into the database.",
)
def sync_analyst_estimates(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS.get("metrics_limit", 10),
        ge=LIMITS.get("metrics_limit", {}).get("min", 1),
        le=LIMITS.get("metrics_limit", {}).get("max", 100),
    ),
    period: str = Query(
        default="quarter", enum=PERIOD_TYPES.get("metrics", ["quarter", "annual"])
    ),
    service: AnalystEstimateSyncService = Depends(get_analyst_estimate_sync_service),
):
    """
    Sync analyst estimates from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('quarter' or 'annual')
        service: AnalystEstimateSyncService instance (injected)

    Returns:
        AnalystEstimateSyncResult: Sync result with status and counts

    Raises:
        HTTPException: 404 if analyst estimates not found
    """
    result = service.upsert_analyst_estimates(symbol=symbol, period=period, limit=limit)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_ANALYST_ESTIMATES"].format(symbol=symbol),
        )

    return result
