from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.quote import StockPriceChangeRead
from app.services.internal.quotes_sync_service import QuotesSyncService

router = APIRouter(prefix="", tags=["quotes_data"])


def get_quotes_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> QuotesSyncService:
    """
    Provides QuotesSyncService with required dependencies.
    """
    return QuotesSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/{symbol}/sync",
    response_model=StockPriceChangeRead,
    summary="Sync company price change from external API",
    description="Fetches and upserts a company's price change from the external API into the database.",
)
async def sync_price_change(
    symbol: str, service: QuotesSyncService = Depends(get_quotes_sync_service)
):
    """
    Sync a company's price change from the external API and store it in the database.

    Args:
        symbol (str): The stock symbol of the company
        service (QuotesSyncService): Injected quotes sync service

    Returns:
        CompanyRatingSummaryRead: The synced rating summary data

    Raises:
        HTTPException: If price change is not found for the symbol
    """
    price_change = service.upsert_price_change(symbol)
    if not price_change:
        raise HTTPException(
            status_code=404, detail=f"Price change not found for symbol: {symbol}"
        )
    return price_change
