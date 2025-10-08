from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_fmp_client, get_db_session
from app.schemas.company import CompanyRead
from app.services.internal.company_sync_service import CompanySyncService

router = APIRouter(prefix="/company")

def get_company_sync_service(
    client: FMPClientProtocol = Depends(get_fmp_client),
    session: Session = Depends(get_db_session),
) -> CompanySyncService:
    return CompanySyncService(market_api_client=client, session=session)


@router.get("/{symbol}/sync", response_model=CompanyRead)
def sync_company_profile(symbol: str, service: CompanySyncService = Depends(get_company_sync_service)):
    company = service.upsert_company(symbol)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company