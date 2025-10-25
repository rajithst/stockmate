from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.rating import CompanyRatingSummaryRead
from app.services.internal.rating_sync_service import RatingSyncService

router = APIRouter(prefix="", tags=["rating_data"])


def get_rating_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> RatingSyncService:
    """
    Provides RatingSyncService with required dependencies.
    """
    return RatingSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/{symbol}/sync",
    response_model=CompanyRatingSummaryRead,
    summary="Sync company rating summary from external API",
    description="Fetches and upserts a company's rating summary from the external API into the database.",
)
async def sync_company_rating_summary(
    symbol: str, service: RatingSyncService = Depends(get_rating_sync_service)
):
    """
    Sync a company's rating summary from the external API and store it in the database.

    Args:
        symbol (str): The stock symbol of the company
        service (RatingSyncService): Injected rating sync service

    Returns:
        CompanyRatingSummaryRead: The synced rating summary data

    Raises:
        HTTPException: If rating summary is not found for the symbol
    """
    rating_summary = service.upsert_rating_summary(symbol)
    if not rating_summary:
        raise HTTPException(
            status_code=404, detail=f"Rating summary not found for symbol: {symbol}"
        )
    return rating_summary
