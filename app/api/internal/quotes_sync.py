from fastapi import APIRouter, Depends, HTTPException

from app.api.internal.config import ERROR_MESSAGES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.quote import StockPriceChangeRead, StockPriceRead
from app.services.internal.quotes_sync_service import QuotesSyncService

router = APIRouter(prefix="", tags=[TAGS["quotes"]["name"]])

# Create dependency provider for QuotesSyncService
get_quotes_sync_service = create_sync_service_provider(QuotesSyncService)


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
            detail=ERROR_MESSAGES["NOT_FOUND_PRICE_CHANGES"].format(symbol=symbol),
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
            detail=ERROR_MESSAGES["NOT_FOUND_DAILY_PRICES"].format(symbol=symbol),
        )
    return daily_prices
