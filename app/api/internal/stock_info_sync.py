from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.dividend import CompanyDividendRead
from app.schemas.stock import CompanyStockSplitRead, CompanyStockPeerRead
from app.services.internal.stock_info_sync_service import StockInfoSyncService

router = APIRouter(prefix="/stock", tags=["Internal Stock Info"])


def get_stock_info_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> StockInfoSyncService:
    """
    Provides StockInfoSyncService with required dependencies.
    """
    return StockInfoSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/dividend/{symbol}/sync",
    response_model=List[CompanyDividendRead],
    summary="Sync company dividends from external API",
    description="Fetches and upserts company's dividend history from the external API into the database.",
)
async def sync_company_dividends(
    symbol: str,
    limit: int = Query(default=100, ge=1, le=1000),
    service: StockInfoSyncService = Depends(get_stock_info_sync_service),
):
    """
    Sync company's dividend history from the external API and store in the database.
    """
    dividends = service.upsert_dividends(symbol, limit)
    if not dividends:
        raise HTTPException(
            status_code=404, detail=f"Dividend history not found for symbol: {symbol}"
        )
    return dividends


@router.get(
    "/split/{symbol}/sync",
    response_model=List[CompanyStockSplitRead],
    summary="Sync company stock splits from external API",
    description="Fetches and upserts company's stock split history from the external API into the database.",
)
async def sync_company_stock_splits(
    symbol: str,
    limit: int = Query(default=100, ge=1, le=1000),
    service: StockInfoSyncService = Depends(get_stock_info_sync_service),
):
    """
    Sync company's stock split history from the external API and store in the database.
    """
    splits = service.upsert_stock_splits(symbol, limit)
    if not splits:
        raise HTTPException(
            status_code=404,
            detail=f"Stock split history not found for symbol: {symbol}",
        )
    return splits


@router.get(
    "/peers/{symbol}/sync",
    response_model=List[CompanyStockPeerRead],
    summary="Sync company stock peers from external API",
    description="Fetches and upserts company's peer information from the external API into the database.",
)
async def sync_company_stock_peers(
    symbol: str, service: StockInfoSyncService = Depends(get_stock_info_sync_service)
):
    """
    Sync company's peer information from the external API and store in the database.
    """
    peers = service.upsert_stock_peers(symbol)
    if not peers:
        raise HTTPException(
            status_code=404, detail=f"Stock peers not found for symbol: {symbol}"
        )
    return peers
