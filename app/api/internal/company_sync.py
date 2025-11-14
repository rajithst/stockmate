from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.company import CompanyRead
from app.services.internal.company_sync_service import CompanySyncService

router = APIRouter(prefix="")

# Create dependency provider for CompanySyncService
get_company_sync_service = create_sync_service_provider(CompanySyncService)


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
