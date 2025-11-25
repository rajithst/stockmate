from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.quote import (
    CompanyDividendRead,
    CompanyStockPeerRead,
    CompanyStockSplitRead,
    IndexQuoteRead,
    StockPriceChangeRead,
    StockPriceRead,
)
from app.services.internal.quotes_sync_service import QuotesSyncService

router = APIRouter(prefix="")

# Create dependency provider for QuotesSyncService
get_quotes_sync_service = create_sync_service_provider(QuotesSyncService)


@router.get(
    "/historical-prices/{symbol}/sync",
    response_model=list[StockPriceRead],
    summary="Sync company historical prices from external API",
    description="Fetches and upserts a company's historical prices from the external API into the database.",
)
def sync_historical_prices(
    symbol: str,
    from_date: str | None = Query(default=None),
    to_date: str | None = Query(default=None),
    service: QuotesSyncService = Depends(get_quotes_sync_service),
):
    """Sync a company's historical prices from the external API and store them in the database."""
    historical_prices = service.upsert_historical_prices(symbol, from_date, to_date)
    if not historical_prices:
        raise HTTPException(
            status_code=404,
            detail="Historical prices not found for symbol: {}".format(symbol),
        )
    return historical_prices


@router.get(
    "/price-change/{symbol}/sync",
    response_model=StockPriceChangeRead,
    summary="Sync company price change from external API",
    description="Fetches and upserts a company's price change from the external API into the database.",
)
def sync_price_change(
    symbol: str, service: QuotesSyncService = Depends(get_quotes_sync_service)
):
    """Sync a company's price change from the external API and store it in the database."""
    price_change = service.upsert_price_change(symbol)
    if not price_change:
        raise HTTPException(
            status_code=404,
            detail="Price change data not found for symbol: {}".format(symbol),
        )
    return price_change


@router.get(
    "/daily-prices/{symbol}/sync",
    response_model=StockPriceRead,
    summary="Sync company daily prices from external API",
    description="Fetches and upserts a company's daily prices from the external API into the database.",
)
def sync_daily_prices(
    symbol: str, service: QuotesSyncService = Depends(get_quotes_sync_service)
):
    """Sync a company's daily prices from the external API and store them in the database."""
    daily_prices = service.upsert_daily_prices(symbol)
    if not daily_prices:
        raise HTTPException(
            status_code=404,
            detail="Daily prices not found for symbol: {}".format(symbol),
        )
    return daily_prices


@router.get(
    "/index-quote/{symbol}/sync",
    response_model=IndexQuoteRead,
    summary="Sync company index quote from external API",
    description="Fetches and upserts a company's index quote from the external API into the database.",
)
def sync_index_quote(
    symbol: str, service: QuotesSyncService = Depends(get_quotes_sync_service)
):
    """Sync a company's index quote from the external API and store it in the database."""
    index_quote = service.upsert_index_quote(symbol)
    if not index_quote:
        raise HTTPException(
            status_code=404,
            detail="Index quote not found for symbol: {}".format(symbol),
        )
    return index_quote


@router.get(
    "/after-hours-price/{symbol}/sync",
    response_model=StockPriceRead,
    summary="Sync company after-hours prices from external API",
    description="Fetches and upserts a company's after-hours prices from the external API into the database.",
)
def sync_after_hours_prices(
    symbol: str, service: QuotesSyncService = Depends(get_quotes_sync_service)
):
    """Sync a company's after-hours prices from the external API and store them in the database."""
    after_hours_prices = service.upsert_after_hours_prices(symbol)
    if not after_hours_prices:
        raise HTTPException(
            status_code=404,
            detail="After-hours prices not found for symbol: {}".format(symbol),
        )
    return after_hours_prices


@router.get(
    "/stock-split/{symbol}/sync",
    response_model=list[CompanyStockSplitRead],
    summary="Sync company stock splits from external API",
    description="Fetches and upserts company's stock split history from the external API into the database.",
)
def sync_stock_splits(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    service: QuotesSyncService = Depends(get_quotes_sync_service),
):
    """Sync company's stock split history from the external API and store in the database."""
    splits = service.upsert_stock_splits(symbol, limit)
    if not splits:
        raise HTTPException(
            status_code=404,
            detail="Stock splits not found for symbol: {}".format(symbol),
        )
    return splits


@router.get(
    "/stock-peers/{symbol}/sync",
    response_model=list[CompanyStockPeerRead],
    summary="Sync company stock peers from external API",
    description="Fetches and upserts company's peer information from the external API into the database.",
)
def sync_stock_peers(
    symbol: str, service: QuotesSyncService = Depends(get_quotes_sync_service)
):
    """Sync company's peer information from the external API and store in the database."""
    peers = service.upsert_stock_peers(symbol)
    if not peers:
        raise HTTPException(
            status_code=404,
            detail="Stock peers not found for symbol: {}".format(symbol),
        )
    return peers


@router.get(
    "/dividend/{symbol}/sync",
    response_model=list[CompanyDividendRead],
    summary="Sync dividends for a specific company from external API",
    description="Fetches and upserts a specific company's dividend history from the external API into the database.",
)
def sync_dividends_for_company(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    service: QuotesSyncService = Depends(get_quotes_sync_service),
):
    """Sync a specific company's dividend history from the external API and store in the database."""
    dividends = service.upsert_dividends(symbol)
    if not dividends:
        raise HTTPException(
            status_code=404,
            detail="Dividends not found for symbol: {}".format(symbol),
        )
    return dividends


@router.get(
    "/dividend-calendar/sync",
    response_model=list[CompanyDividendRead],
    summary="Sync company dividends from external API",
    description="Fetches and upserts company's dividend history from the external API into the database.",
)
def sync_dividends(
    from_date: str | None = Query(default=None),
    to_date: str | None = Query(default=None),
    service: QuotesSyncService = Depends(get_quotes_sync_service),
):
    """Sync company's dividend history from the external API and store in the database."""
    dividends = service.upsert_dividend_calendar(from_date, to_date)
    if not dividends:
        raise HTTPException(
            status_code=404,
            detail="Dividends not found",
        )
    return dividends
