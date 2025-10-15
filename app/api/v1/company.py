from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.schemas.company import CompanyPageResponse
from app.services.company_page_service import CompanyPageService

router = APIRouter(prefix="/company")


def get_company_service(
    session: Session = Depends(get_db_session),
) -> CompanyPageService:
    return CompanyPageService(session=session)


@router.get("/{symbol}", response_model=CompanyPageResponse)
def get_company_profile(
    symbol: str, service: CompanyPageService = Depends(get_company_service)
):
    page = service.get_company_page(symbol)
    if not page:
        raise HTTPException(status_code=404, detail="Company not found")
    return page
