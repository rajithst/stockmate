import logging

from fastapi import APIRouter, Depends, HTTPException

from app.db.engine import SessionLocal
from app.models.company import CompanyProfileRead
from app.services.company_service import CompanyService

router = APIRouter(prefix="/company")

def get_company_service() -> CompanyService:
    return CompanyService(session=SessionLocal())

@router.get("/profile/{symbol}", response_model=CompanyProfileRead)
def get_company_profile(symbol: str, service: CompanyService = Depends(get_company_service)):
    company = service.get_company_profile(symbol)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company