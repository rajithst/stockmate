from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.dcf import DiscountedCashFlowRead
from app.services.internal.dcf_sync_service import DiscountedCashFlowSyncService

router = APIRouter(prefix="", tags=["dcf_data"])


def get_dcf_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> DiscountedCashFlowSyncService:
    """
    Provides DiscountedCashFlowSyncService with required dependencies.
    """
    return DiscountedCashFlowSyncService(
        market_api_client=fmp_client, session=db_session
    )


@router.get(
    "/{symbol}/sync",
    response_model=DiscountedCashFlowRead,
    summary="Sync company discounted cash flow from external API",
    description="Fetches and upserts company's discounted cash flow from the external API into the database.",
)
async def sync_company_discounted_cash_flow(
    symbol: str,
    service: DiscountedCashFlowSyncService = Depends(get_dcf_sync_service),
):
    """
    Sync company's discounted cash flow from the external API and store in the database.
    """
    statements = service.upsert_discounted_cash_flow(symbol)
    if not statements:
        raise HTTPException(
            status_code=404,
            detail=f"Discounted cash flow not found for symbol: {symbol}",
        )
    return statements
