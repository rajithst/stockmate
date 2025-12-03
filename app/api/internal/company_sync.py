from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.sync_services import get_company_sync_service
from app.schemas.company import CompanyRead, NonUSCompanyRead
from app.services.internal.company_sync_service import CompanySyncService

router = APIRouter(prefix="")


@router.get(
    "/{symbol}/sync",
    response_model=CompanyRead,
    summary="Sync company profile from external API",
    description="Fetches and upserts a company's profile from the external API into the database.",
)
def sync_company_profile(
    symbol: str, service: CompanySyncService = Depends(get_company_sync_service)
):
    """
    Sync a company's profile from the external API and store it in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        service: CompanySyncService instance (injected)

    Returns:
        CompanyRead: Synced company data

    Raises:
        HTTPException: 404 if company not found
    """
    company = service.upsert_company(symbol)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found for symbol: {}".format(symbol),
        )
    return company


@router.get(
    "/non-us/{symbol}/sync",
    response_model=NonUSCompanyRead,
    summary="Sync non-US company profile from external API",
    description="Fetches and upserts a non-US company's profile from the external API into the database.",
)
def sync_non_us_company_profile(
    symbol: str, service: CompanySyncService = Depends(get_company_sync_service)
):
    """
    Sync a non-US company's profile from the external API and store it in the database.

    Args:
        symbol: Stock symbol (e.g., '7203.T')
        service: CompanySyncService instance (injected)
    Returns:
        CompanyRead: Synced non-US company data
    Raises:
        HTTPException: 404 if company not found
    """
    company = service.upsert_non_us_company(symbol)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found for symbol: {}".format(symbol),
        )
    return company
