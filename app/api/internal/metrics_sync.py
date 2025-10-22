from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.financial_ratio import FinancialRatioRead
from app.schemas.financial_score import CompanyFinancialScoresRead
from app.schemas.key_metrics import CompanyKeyMetricsRead
from app.services.internal.metrics_sync_service import MetricsSyncService

router = APIRouter(prefix="/metrics", tags=["Internal Metrics"])


def get_metrics_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> MetricsSyncService:
    """
    Provides MetricsSyncService with required dependencies.
    """
    return MetricsSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/key-metrics/{symbol}/sync",
    response_model=List[CompanyKeyMetricsRead],
    summary="Sync company key metrics from external API",
    description="Fetches and upserts company's key metrics from the external API into the database.",
)
async def sync_company_key_metrics(
    symbol: str,
    limit: int = Query(default=40, ge=1, le=100),
    period: str = Query(
        default="quarter", enum=["Q1", "Q2", "Q3", "Q4", "FY", "annual", "quarter"]
    ),
    service: MetricsSyncService = Depends(get_metrics_sync_service),
):
    """
    Sync company's key metrics from the external API and store in the database.
    """
    metrics = service.upsert_key_metrics(symbol, limit, period)
    if not metrics:
        raise HTTPException(
            status_code=404, detail=f"Key metrics not found for symbol: {symbol}"
        )
    return metrics


@router.get(
    "/financial-ratios/{symbol}/sync",
    response_model=List[FinancialRatioRead],
    summary="Sync company financial ratios from external API",
    description="Fetches and upserts company's financial ratios from the external API into the database.",
)
async def sync_company_financial_ratios(
    symbol: str,
    limit: int = Query(default=40, ge=1, le=100),
    period: str = Query(
        default="quarter", enum=["Q1", "Q2", "Q3", "Q4", "FY", "annual", "quarter"]
    ),
    service: MetricsSyncService = Depends(get_metrics_sync_service),
):
    """
    Sync company's financial ratios from the external API and store in the database.
    """
    ratios = service.upsert_financial_ratios(symbol, limit, period)
    if not ratios:
        raise HTTPException(
            status_code=404, detail=f"Financial ratios not found for symbol: {symbol}"
        )
    return ratios


@router.get(
    "/financial-scores/{symbol}/sync",
    response_model=CompanyFinancialScoresRead,
    summary="Sync company financial scores from external API",
    description="Fetches and upserts company's financial scores from the external API into the database.",
)
async def sync_company_financial_scores(
    symbol: str, service: MetricsSyncService = Depends(get_metrics_sync_service)
):
    """
    Sync company's financial scores from the external API and store in the database.
    """
    scores = service.upsert_financial_scores(symbol)
    if not scores:
        raise HTTPException(
            status_code=404, detail=f"Financial scores not found for symbol: {symbol}"
        )
    return scores
