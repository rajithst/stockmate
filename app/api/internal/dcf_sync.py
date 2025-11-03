from fastapi import APIRouter, Depends, HTTPException

from app.api.internal.config import ERROR_MESSAGES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.dcf import DiscountedCashFlowRead
from app.services.internal.dcf_sync_service import DiscountedCashFlowSyncService

router = APIRouter(prefix="", tags=[TAGS["dcf"]["name"]])

# Create dependency provider for DiscountedCashFlowSyncService
get_dcf_sync_service = create_sync_service_provider(DiscountedCashFlowSyncService)


@router.get(
    "/{symbol}/sync",
    response_model=DiscountedCashFlowRead,
    summary="Sync company DCF valuation from external API",
    description="Fetches and upserts company's discounted cash flow valuation from the external API into the database.",
)
def sync_company_dcf(
    symbol: str, service: DiscountedCashFlowSyncService = Depends(get_dcf_sync_service)
):
    """
    Sync company's discounted cash flow valuation from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        service: DiscountedCashFlowSyncService instance (injected)

    Returns:
        DiscountedCashFlowRead: Synced DCF valuation data

    Raises:
        HTTPException: 404 if DCF data not found
    """
    dcf_data = service.upsert_discounted_cash_flow(symbol)
    if not dcf_data:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_DCF"].format(symbol=symbol),
        )
    return dcf_data
