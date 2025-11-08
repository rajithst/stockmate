from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.internal.config import DEFAULTS, ERROR_MESSAGES, LIMITS, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.quote import CompanyDividendRead
from app.schemas.quote import CompanyStockSplitRead, CompanyStockPeerRead
from app.services.internal.stock_info_sync_service import StockInfoSyncService

router = APIRouter(prefix="", tags=[TAGS["stock_info"]["name"]])

# Create dependency provider for StockInfoSyncService
get_stock_info_sync_service = create_sync_service_provider(StockInfoSyncService)


@router.get(
    "/dividend/sync",
    response_model=list[CompanyDividendRead],
    summary="Sync company dividends from external API",
    description="Fetches and upserts company's dividend history from the external API into the database.",
)
def sync_dividends(
    service: StockInfoSyncService = Depends(get_stock_info_sync_service),
):
    """Sync company's dividend history from the external API and store in the database."""
    dividends = service.upsert_dividend_calendar()
    if not dividends:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_DIVIDENDS"],
        )
    return dividends


@router.get(
    "/dividend/{symbol}/sync",
    response_model=list[CompanyDividendRead],
    summary="Sync dividends for a specific company from external API",
    description="Fetches and upserts a specific company's dividend history from the external API into the database.",
)
def sync_dividends_for_company(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["stock_info_limit"],
        ge=LIMITS["stock_info_limit"]["min"],
        le=LIMITS["stock_info_limit"]["max"],
    ),
    service: StockInfoSyncService = Depends(get_stock_info_sync_service),
):
    """Sync a specific company's dividend history from the external API and store in the database."""
    dividends = service.upsert_dividends(symbol)
    if not dividends:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_DIVIDENDS"],
        )
    return dividends


@router.get(
    "/split/{symbol}/sync",
    response_model=list[CompanyStockSplitRead],
    summary="Sync company stock splits from external API",
    description="Fetches and upserts company's stock split history from the external API into the database.",
)
def sync_stock_splits(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["stock_info_limit"],
        ge=LIMITS["stock_info_limit"]["min"],
        le=LIMITS["stock_info_limit"]["max"],
    ),
    service: StockInfoSyncService = Depends(get_stock_info_sync_service),
):
    """Sync company's stock split history from the external API and store in the database."""
    splits = service.upsert_stock_splits(symbol, limit)
    if not splits:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_STOCK_SPLITS"].format(symbol=symbol),
        )
    return splits


@router.get(
    "/peers/{symbol}/sync",
    response_model=list[CompanyStockPeerRead],
    summary="Sync company stock peers from external API",
    description="Fetches and upserts company's peer information from the external API into the database.",
)
def sync_stock_peers(
    symbol: str, service: StockInfoSyncService = Depends(get_stock_info_sync_service)
):
    """Sync company's peer information from the external API and store in the database."""
    peers = service.upsert_stock_peers(symbol)
    if not peers:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_STOCK_PEERS"].format(symbol=symbol),
        )
    return peers
