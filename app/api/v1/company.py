from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.schemas.company import (
    CompanyFinancialHealthResponse,
    CompanyFinancialResponse,
    CompanyPageResponse,
)
from app.schemas.technical_indicator import CompanyTechnicalIndicatorRead
from app.services.company_service import CompanyService

router = APIRouter(prefix="")


def get_company_service(
    session: Session = Depends(get_db_session),
) -> CompanyService:
    return CompanyService(session=session)


@router.get("/{symbol}", response_model=CompanyPageResponse)
def get_company_profile(
    symbol: str, service: CompanyService = Depends(get_company_service)
):
    page = service.get_company_page(symbol)
    if not page:
        raise HTTPException(status_code=404, detail="Company not found")
    return page


@router.get("/{symbol}/financials", response_model=CompanyFinancialResponse)
def get_company_financials(
    symbol: str, service: CompanyService = Depends(get_company_service)
):
    page = service.get_company_financials(symbol)
    if not page:
        raise HTTPException(status_code=404, detail="Company not found")
    return page


@router.get("/{symbol}/financial-health", response_model=CompanyFinancialHealthResponse)
def get_company_financial_health(
    symbol: str, service: CompanyService = Depends(get_company_service)
):
    page = service.get_company_financial_health(symbol)
    if not page:
        raise HTTPException(status_code=404, detail="Company not found")
    return page


@router.get(
    "/{symbol}/technical-indicators", response_model=CompanyTechnicalIndicatorRead
)
def get_company_technical_indicators(
    symbol: str, service: CompanyService = Depends(get_company_service)
):
    page = service.get_company_technical_indicators(symbol)
    if not page:
        raise HTTPException(status_code=404, detail="Company not found")
    return page
