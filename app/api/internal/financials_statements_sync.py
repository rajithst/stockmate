from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.financial_statements import (
    CompanyBalanceSheetRead,
    CompanyCashFlowStatementRead,
    CompanyFinancialRatioRead,
    CompanyIncomeStatementRead,
)
from app.services.internal.financial_statements_sync_service import (
    CompanyFinancialStatementsSyncService,
)

router = APIRouter(prefix="")

# Create dependency provider for FinancialSyncService
get_financials_sync_service = create_sync_service_provider(
    CompanyFinancialStatementsSyncService
)


@router.get(
    "/balance-sheet/{symbol}/sync",
    response_model=list[CompanyBalanceSheetRead],
    summary="Sync company balance sheets from external API",
    description="Fetches and upserts company's balance sheets from the external API into the database.",
)
def sync_balance_sheets(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    period: str = Query(default="quarter", enum=["annual", "quarter"]),
    service: CompanyFinancialStatementsSyncService = Depends(
        get_financials_sync_service
    ),
):
    """
    Sync company's balance sheets from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('annual' or 'quarter')
        service: FinancialSyncService instance (injected)

    Returns:
        list[CompanyBalanceSheetRead]: Synced balance sheet records

    Raises:
        HTTPException: 404 if balance sheets not found
    """
    statements = service.upsert_balance_sheets(symbol, limit, period)
    if not statements:
        raise HTTPException(
            status_code=404,
            detail="Balance sheets not found for symbol: {}".format(symbol),
        )
    return statements


@router.get(
    "/income-statement/{symbol}/sync",
    response_model=list[CompanyIncomeStatementRead],
    summary="Sync company income statements from external API",
    description="Fetches and upserts company's income statements from the external API into the database.",
)
def sync_income_statements(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    period: str = Query(default="quarter", enum=["annual", "quarter"]),
    service: CompanyFinancialStatementsSyncService = Depends(
        get_financials_sync_service
    ),
):
    """
    Sync company's income statements from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('annual' or 'quarter')
        service: FinancialSyncService instance (injected)

    Returns:
        list[CompanyIncomeStatementRead]: Synced income statement records

    Raises:
        HTTPException: 404 if income statements not found
    """
    statements = service.upsert_income_statements(symbol, limit, period)
    if not statements:
        raise HTTPException(
            status_code=404,
            detail="Income statements not found for symbol: {}".format(symbol),
        )
    return statements


@router.get(
    "/cash-flow/{symbol}/sync",
    response_model=list[CompanyCashFlowStatementRead],
    summary="Sync company cash flow statements from external API",
    description="Fetches and upserts company's cash flow statements from the external API into the database.",
)
def sync_cash_flow_statements(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    period: str = Query(default="quarter", enum=["annual", "quarter"]),
    service: CompanyFinancialStatementsSyncService = Depends(
        get_financials_sync_service
    ),
):
    """
    Sync company's cash flow statements from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('annual' or 'quarter')
        service: FinancialSyncService instance (injected)

    Returns:
        list[CompanyCashFlowStatementRead]: Synced cash flow statement records

    Raises:
        HTTPException: 404 if cash flow statements not found
    """
    statements = service.upsert_cash_flow_statements(symbol, limit, period)
    if not statements:
        raise HTTPException(
            status_code=404,
            detail="Cash flow statements not found for symbol: {}".format(symbol),
        )
    return statements


@router.get(
    "/financial-ratios/{symbol}/sync",
    response_model=list[CompanyFinancialRatioRead],
    summary="Sync company financial ratios from external API",
    description="Fetches and upserts company's financial ratios from the external API into the database.",
)
def sync_financial_ratios(
    symbol: str,
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    period: str = Query(default="quarter", enum=["annual", "quarter"]),
    service: CompanyFinancialStatementsSyncService = Depends(
        get_financials_sync_service
    ),
):
    """
    Sync company's financial ratios from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        limit: Number of records to fetch (1-100)
        period: Period type ('annual' or 'quarter')
        service: CompanyFinancialStatementsSyncService instance (injected)

    Returns:
        list[CompanyFinancialRatioRead]: Synced financial ratio records

    Raises:
        HTTPException: 404 if financial ratios not found
    """
    ratios = service.upsert_financial_ratios(symbol, limit, period)
    if not ratios:
        raise HTTPException(
            status_code=404,
            detail="Financial ratios not found for symbol: {}".format(symbol),
        )
    return ratios


@router.get(
    "/financial-ratios-ttm/{symbol}/sync",
    response_model=CompanyFinancialRatioRead,
    summary="Sync company trailing twelve months financial ratios from external API",
    description="Fetches and upserts company's trailing twelve months financial ratios from the external API into the database.",
)
def sync_financial_ratios_ttm(
    symbol: str,
    service: CompanyFinancialStatementsSyncService = Depends(
        get_financials_sync_service
    ),
):
    """
    Sync company's trailing twelve months financial ratios from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        service: CompanyFinancialStatementsSyncService instance (injected)
    Returns:
        CompanyFinancialRatioRead: Synced financial ratio record
    Raises:
        HTTPException: 404 if financial ratios not found
    """
    ratio = service.upsert_financial_ratios_ttm(symbol)
    if not ratio:
        raise HTTPException(
            status_code=404,
            detail="Financial ratios (TTM) not found for symbol: {}".format(symbol),
        )
    return ratio
