from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.internal.config import DEFAULTS, ERROR_MESSAGES, LIMITS, PERIOD_TYPES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.financial_statements import CompanyBalanceSheetRead
from app.schemas.financial_statements import CompanyCashFlowStatementRead
from app.schemas.financial_health import CompanyFinancialHealthRead
from app.schemas.financial_statements import CompanyIncomeStatementRead
from app.services.internal.financial_sync_service import FinancialSyncService

router = APIRouter(prefix="", tags=[TAGS["financial"]["name"]])

# Create dependency provider for FinancialSyncService
get_financials_sync_service = create_sync_service_provider(FinancialSyncService)


@router.get(
    "/balance-sheet/{symbol}/sync",
    response_model=list[CompanyBalanceSheetRead],
    summary="Sync company balance sheets from external API",
    description="Fetches and upserts company's balance sheets from the external API into the database.",
)
def sync_balance_sheets(
    symbol: str,
    limit: int = Query(
        default=DEFAULTS["financial_limit"],
        ge=LIMITS["financial_limit"]["min"],
        le=LIMITS["financial_limit"]["max"],
    ),
    period: str = Query(default="quarter", enum=PERIOD_TYPES["financial"]),
    service: FinancialSyncService = Depends(get_financials_sync_service),
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
            detail=ERROR_MESSAGES["NOT_FOUND_BALANCE_SHEETS"].format(symbol=symbol),
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
        default=DEFAULTS["financial_limit"],
        ge=LIMITS["financial_limit"]["min"],
        le=LIMITS["financial_limit"]["max"],
    ),
    period: str = Query(default="quarter", enum=PERIOD_TYPES["financial"]),
    service: FinancialSyncService = Depends(get_financials_sync_service),
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
            detail=ERROR_MESSAGES["NOT_FOUND_INCOME_STATEMENTS"].format(symbol=symbol),
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
        default=DEFAULTS["financial_limit"],
        ge=LIMITS["financial_limit"]["min"],
        le=LIMITS["financial_limit"]["max"],
    ),
    period: str = Query(default="quarter", enum=PERIOD_TYPES["financial"]),
    service: FinancialSyncService = Depends(get_financials_sync_service),
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
            detail=ERROR_MESSAGES["NOT_FOUND_CASH_FLOW"].format(symbol=symbol),
        )
    return statements


@router.get(
    "/financial-health/{symbol}/sync",
    response_model=list[CompanyFinancialHealthRead],
    summary="Sync company financial health data from external API",
    description="Fetches and upserts company's financial health data from the external API into the database.",
)
def sync_financial_health(
    symbol: str,
    service: FinancialSyncService = Depends(get_financials_sync_service),
):
    """
    Sync company's financial health data from the external API and store in the database.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        service: FinancialSyncService instance (injected)

    Returns:
        list[CompanyFinancialHealthRead]: Synced financial health records

    Raises:
        HTTPException: 404 if financial health data not found
    """
    health_data = service.upsert_financial_health(symbol)
    if not health_data:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_FINANCIAL_HEALTH"].format(symbol=symbol),
        )
    return health_data
