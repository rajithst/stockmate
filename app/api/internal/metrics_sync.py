from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.internal.config import DEFAULTS, ERROR_MESSAGES, LIMITS, PERIOD_TYPES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.financial_statements import CompanyFinancialRatioRead
from app.schemas.financial_health import CompanyFinancialScoresRead
from app.schemas.company_metrics import CompanyKeyMetricsRead
from app.services.internal.metrics_sync_service import MetricsSyncService

router = APIRouter(prefix="", tags=[TAGS["metrics"]["name"]])

# Create dependency provider for MetricsSyncService
get_metrics_sync_service = create_sync_service_provider(MetricsSyncService)


@router.get(
    "/key-metrics/{symbol}/sync",
    response_model=list[CompanyKeyMetricsRead],
    summary="Sync company key metrics from external API",
    description="Fetches and upserts company's key metrics from the external API into the database.",
)
def sync_key_metrics(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["metrics_limit"],
        ge=LIMITS["metrics_limit"]["min"],
        le=LIMITS["metrics_limit"]["max"],
    ),
    period: str = Query(default="quarter", enum=PERIOD_TYPES["metrics"]),
    service: MetricsSyncService = Depends(get_metrics_sync_service),
):
    """
    Sync company's key metrics from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('annual' or 'quarter')
        service: MetricsSyncService instance (injected)

    Returns:
        list[CompanyKeyMetricsRead]: Synced key metrics records

    Raises:
        HTTPException: 404 if key metrics not found
    """
    metrics = service.upsert_key_metrics(symbol, limit, period)
    if not metrics:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_KEY_METRICS"].format(symbol=symbol),
        )
    return metrics


@router.get(
    "/financial-ratios/{symbol}/sync",
    response_model=list[CompanyFinancialRatioRead],
    summary="Sync company financial ratios from external API",
    description="Fetches and upserts company's financial ratios from the external API into the database.",
)
def sync_financial_ratios(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["metrics_limit"],
        ge=LIMITS["metrics_limit"]["min"],
        le=LIMITS["metrics_limit"]["max"],
    ),
    period: str = Query(default="quarter", enum=PERIOD_TYPES["metrics"]),
    service: MetricsSyncService = Depends(get_metrics_sync_service),
):
    """
    Sync company's financial ratios from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('annual' or 'quarter')
        service: MetricsSyncService instance (injected)

    Returns:
        list[CompanyFinancialRatioRead]: Synced financial ratio records

    Raises:
        HTTPException: 404 if financial ratios not found
    """
    ratios = service.upsert_financial_ratios(symbol, limit, period)
    if not ratios:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_FINANCIAL_RATIOS"].format(symbol=symbol),
        )
    return ratios


@router.get(
    "/financial-scores/{symbol}/sync",
    response_model=CompanyFinancialScoresRead,
    summary="Sync company financial scores from external API",
    description="Fetches and upserts company's financial scores from the external API into the database.",
)
def sync_financial_scores(
    symbol: str, service: MetricsSyncService = Depends(get_metrics_sync_service)
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
            detail=ERROR_MESSAGES["NOT_FOUND_FINANCIAL_SCORES"].format(symbol=symbol),
        )
    return scores
