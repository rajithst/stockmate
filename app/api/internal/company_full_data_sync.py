from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.internal.config import TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.services.internal.company_full_data_sync_service import (
    CompanyFullDataSyncService,
)

router = APIRouter(prefix="", tags=[TAGS["company"]["name"]])

# Create dependency provider for CompanyFullDataSyncService
get_company_full_sync_service = create_sync_service_provider(CompanyFullDataSyncService)


@router.get(
    "/{symbol}/sync-all",
    summary="Sync all company data from external API",
    description="Fetches and upserts all company data (profile, quotes, financials, etc.) from the external API into the database. Includes sleep between API calls to respect rate limits.",
)
def sync_all_company_data(
    symbol: str,
    financial_limit: int = Query(default=40, ge=1, le=100),
    metrics_limit: int = Query(default=40, ge=1, le=100),
    sleep_time: float = Query(default=0.5, ge=0, le=5),
    include_news: bool = Query(default=False),
    service: CompanyFullDataSyncService = Depends(get_company_full_sync_service),
):
    """
    Sync all company data from the external API and store in the database.

    This endpoint orchestrates syncing of multiple data types in sequence:
    1. Company profile
    2. Price change
    3. Price targets
    4. Ratings
    5. Gradings
    6. DCF valuation
    7. Key metrics
    8. Financial ratios
    9. Income statements
    10. Balance sheets
    11. Cash flow statements
    12. Stock peers
    13. Stock splits

    Note: This is a debug endpoint for quickly filling company data. It may take
    several seconds due to multiple API calls with sleep intervals.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        financial_limit: Number of financial records to fetch (1-100)
        metrics_limit: Number of metric records to fetch (1-100)
        sleep_time: Sleep duration between API calls in seconds (0-5)
        include_news: Whether to sync company news (slower)
        service: CompanyFullDataSyncService instance (injected)

    Returns:
        Dictionary with detailed sync results including:
        - symbol: Stock symbol synced
        - status: Overall status (success, partial, failed)
        - steps: Dictionary showing result of each sync step
        - total_api_calls: Number of API calls made
        - total_time_seconds: Total time taken

    Raises:
        HTTPException: 500 if fatal error during sync
    """
    try:
        result = service.sync_all_company_data(
            symbol=symbol,
            financial_limit=financial_limit,
            metrics_limit=metrics_limit,
            include_news=include_news,
        )

        if result.get("status") == "failed":
            raise HTTPException(
                status_code=500,
                detail=f"Failed to sync company data: {result.get('error', 'Unknown error')}",
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during company data sync: {str(e)}",
        )
