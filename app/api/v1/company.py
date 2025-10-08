from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.schemas.company import CompanyRead
from app.services.company_service import CompanyService

router = APIRouter(prefix="/company")

def get_company_service(
    session: Session = Depends(get_db_session),
) -> CompanyService:
    return CompanyService(session=session)

@router.get("/{symbol}", response_model=CompanyRead)
def get_company_profile(symbol: str, service: CompanyService = Depends(get_company_service)):
    company = service.get_company_profile(symbol)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company