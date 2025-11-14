from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.financial_health import (
    CompanyFinancialHealthRead,
    CompanyFinancialScoresRead,
)
from app.services.internal.financial_health_sync_service import (
    CompanyFinancialHealthSyncService,
)

router = APIRouter(prefix="")

get_financials_sync_service = create_sync_service_provider(
    CompanyFinancialHealthSyncService
)


@router.get(
    "/financial-health/{symbol}/sync",
    response_model=list[CompanyFinancialHealthRead],
    summary="Sync company financial health data from external API",
    description="Fetches and upserts company's financial health data from the external API into the database.",
)
def sync_financial_health(
    symbol: str,
    service: CompanyFinancialHealthSyncService = Depends(get_financials_sync_service),
):
    """
    Sync company's financial health data from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        service: FinancialSyncService instance (injected)

    Returns:
        list[CompanyFinancialHealthRead]: Synced financial health records

    Raises:
        HTTPException: 404 if financial health data not found
    """
    health_data = service.upsert_financial_health(symbol)
    if not health_data:
        raise HTTPException(
            status_code=404,
            detail="Financial health data not found for symbol: {}".format(symbol),
        )
    return health_data


@router.get(
    "/financial-scores/{symbol}/sync",
    response_model=CompanyFinancialScoresRead,
    summary="Sync company financial scores from external API",
    description="Fetches and upserts company's financial scores from the external API into the database.",
)
def sync_financial_scores(
    symbol: str,
    service: CompanyFinancialHealthSyncService = Depends(get_financials_sync_service),
):
    """
    Sync company's financial scores from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        service: MetricsSyncService instance (injected)

    Returns:
        CompanyFinancialScoresRead: Synced financial scores record

    Raises:
        HTTPException: 404 if financial scores not found
    """
    scores = service.upsert_financial_scores(symbol)
    if not scores:
        raise HTTPException(
            status_code=404,
            detail="Financial scores not found for symbol: {}".format(symbol),
        )
    return scores
