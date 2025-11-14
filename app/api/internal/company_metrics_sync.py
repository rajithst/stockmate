from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.company_metrics import (
    CompanyAnalystEstimateRead,
    CompanyDiscountedCashFlowRead,
    CompanyKeyMetricsRead,
    CompanyRevenueProductSegmentationRead,
)
from app.services.internal.company_metrics_sync_service import (
    CompanyMetricsSyncService,
)

router = APIRouter(
    prefix="",
)

# Create dependency provider for AnalystEstimateSyncService
company_metrics_sync_service = create_sync_service_provider(CompanyMetricsSyncService)


@router.get(
    "/analyst-estimates/{symbol}/sync",
    response_model=list[CompanyAnalystEstimateRead],
    summary="Sync analyst estimates from external API",
    description="Fetches and upserts analyst estimates from the external API into the database.",
)
def sync_analyst_estimates(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    period: str = Query(default="quarter", enum=["quarter", "annual"]),
    service: CompanyMetricsSyncService = Depends(company_metrics_sync_service),
):
    """
    Sync analyst estimates from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('quarter' or 'annual')
        service: CompanyMetricsSyncService instance (injected)

    Returns:
        AnalystEstimateSyncResult: Sync result with status and counts

    Raises:
        HTTPException: 404 if analyst estimates not found
    """
    result = service.upsert_analyst_estimates(symbol=symbol, period=period, limit=limit)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Analyst estimates not found for symbol: {}".format(symbol),
        )

    return result


@router.get(
    "/key-metrics/{symbol}/sync",
    response_model=list[CompanyKeyMetricsRead],
    summary="Sync company key metrics from external API",
    description="Fetches and upserts company's key metrics from the external API into the database.",
)
def sync_key_metrics(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    period: str = Query(default="quarter", enum=["quarter", "annual"]),
    service: CompanyMetricsSyncService = Depends(company_metrics_sync_service),
):
    """
    Sync company's key metrics from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('annual' or 'quarter')
        service: CompanyMetricsSyncService instance (injected)

    Returns:
        list[CompanyKeyMetricsRead]: Synced key metrics records

    Raises:
        HTTPException: 404 if key metrics not found
    """
    metrics = service.upsert_key_metrics(symbol, limit, period)
    if not metrics:
        raise HTTPException(
            status_code=404,
            detail="Key metrics not found for symbol: {}".format(symbol),
        )
    return metrics


@router.get(
    "/dcf/{symbol}/sync",
    response_model=CompanyDiscountedCashFlowRead,
    summary="Sync company DCF valuation from external API",
    description="Fetches and upserts company's discounted cash flow valuation from the external API into the database.",
)
def sync_company_dcf(
    symbol: str,
    service: CompanyMetricsSyncService = Depends(company_metrics_sync_service),
):
    """
    Sync company's discounted cash flow valuation from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        service: CompanyMetricsSyncService instance (injected)

    Returns:
        CompanyDiscountedCashFlowRead: Synced DCF valuation data

    Raises:
        HTTPException: 404 if DCF data not found
    """
    dcf_data = service.upsert_discounted_cash_flow(symbol)
    if not dcf_data:
        raise HTTPException(
            status_code=404,
            detail="Discounted cash flow data not found for symbol: {}".format(symbol),
        )
    return dcf_data


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
    service: CompanyMetricsSyncService = Depends(company_metrics_sync_service),
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
            detail="Revenue product segmentation not found for symbol: {}".format(
                symbol
            ),
        )

    return result
