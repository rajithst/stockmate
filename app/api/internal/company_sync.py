from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.company import CompanyRead
from app.services.internal.company_sync_service import CompanySyncService

router = APIRouter(prefix="/company", tags=["Internal Company"])


def get_company_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> CompanySyncService:
    """Provides CompanySyncService with required dependencies."""
    return CompanySyncService(market_api_client=fmp_client, session=db_session)


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
    """
    company = service.upsert_company(symbol)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
