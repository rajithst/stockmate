from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.sync_services import get_company_service
from app.schemas.company import (
    CompanyFinancialHealthResponse,
    CompanyFinancialResponse,
    CompanyInsightsResponse,
    CompanyPageResponse,
    NonUSCompany,
)
from app.schemas.quote import CompanyTechnicalIndicatorRead
from app.services.company_service import CompanyService

router = APIRouter(prefix="")


@router.get("/{symbol}", response_model=CompanyPageResponse)
def get_company_profile(
    symbol: str, service: CompanyService = Depends(get_company_service)
):
    page = service.get_company_page(symbol)
    if not page:
        raise HTTPException(status_code=404, detail="Company not found")
    return page


@router.get("/non-us/{symbol}", response_model=NonUSCompany)
def get_non_us_company_profile(
    symbol: str, service: CompanyService = Depends(get_company_service)
):
    page = service.get_non_us_company_page(symbol)
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


@router.get("/{symbol}/insights", response_model=CompanyInsightsResponse)
def get_company_insights(
    symbol: str, service: CompanyService = Depends(get_company_service)
):
    insights = service.get_company_insights(symbol)
    if not insights:
        raise HTTPException(status_code=404, detail="Company not found")
    return insights
