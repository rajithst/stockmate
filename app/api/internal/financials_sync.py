from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.balance_sheet import CompanyBalanceSheetRead
from app.schemas.cashflow import CompanyCashFlowStatementRead
from app.schemas.income_statement import CompanyIncomeStatementRead
from app.services.internal.financial_sync_service import FinancialSyncService

router = APIRouter(prefix="", tags=["financial_data"])

period_options = ["Q1", "Q2", "Q3", "Q4", "FY", "annual", "quarter"]


def get_financials_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> FinancialSyncService:
    """
    Provides FinancialSyncService with required dependencies.
    """
    return FinancialSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/balance-sheet/{symbol}/sync",
    response_model=List[CompanyBalanceSheetRead],
    summary="Sync company balance sheets from external API",
    description="Fetches and upserts company's balance sheets from the external API into the database.",
)
async def sync_company_balance_sheets(
    symbol: str,
    limit: int = Query(default=40, ge=1, le=100),
    period: str = Query(default="quarter", enum=period_options),
    service: FinancialSyncService = Depends(get_financials_sync_service),
):
    """
    Sync company's balance sheets from the external API and store in the database.
    """
    statements = service.upsert_balance_sheets(symbol, limit, period)
    if not statements:
        raise HTTPException(
            status_code=404, detail=f"Balance sheets not found for symbol: {symbol}"
        )
    return statements


@router.get(
    "/income-statement/{symbol}/sync",
    response_model=List[CompanyIncomeStatementRead],
    summary="Sync company income statements from external API",
    description="Fetches and upserts company's income statements from the external API into the database.",
)
async def sync_company_income_statements(
    symbol: str,
    limit: int = Query(default=40, ge=1, le=100),
    period: str = Query(default="quarter", enum=period_options),
    service: FinancialSyncService = Depends(get_financials_sync_service),
):
    """
    Sync company's income statements from the external API and store in the database.
    """
    statements = service.upsert_income_statements(symbol, limit, period)
    if not statements:
        raise HTTPException(
            status_code=404, detail=f"Income statements not found for symbol: {symbol}"
        )
    return statements


@router.get(
    "/cash-flow/{symbol}/sync",
    response_model=List[CompanyCashFlowStatementRead],
    summary="Sync company cash flow statements from external API",
    description="Fetches and upserts company's cash flow statements from the external API into the database.",
)
async def sync_company_cash_flow_statements(
    symbol: str,
    limit: int = Query(default=40, ge=1, le=100),
    period: str = Query(default="quarter", enum=period_options),
    service: FinancialSyncService = Depends(get_financials_sync_service),
):
    """
    Sync company's cash flow statements from the external API and store in the database.
    """
    statements = service.upsert_cash_flow_statements(symbol, limit, period)
    if not statements:
        raise HTTPException(
            status_code=404,
            detail=f"Cash flow statements not found for symbol: {symbol}",
        )
    return statements
