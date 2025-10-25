from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies import get_db_session, get_fmp_client
from app.schemas.grading import CompanyGradingRead, CompanyGradingSummaryRead
from app.services.internal.grading_sync_service import GradingSyncService

router = APIRouter(prefix="", tags=["grading_data"])


def get_grading_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> GradingSyncService:
    """
    Provides GradingSyncService with required dependencies.
    """
    return GradingSyncService(market_api_client=fmp_client, session=db_session)


@router.get(
    "/{symbol}/sync",
    response_model=List[CompanyGradingRead],
    summary="Sync company grading from external API",
    description="Fetches and upserts a company's grading data from the external API into the database.",
)
async def sync_company_grading(
    symbol: str, service: GradingSyncService = Depends(get_grading_sync_service)
):
    """
    Sync a company's grading data from the external API and store it in the database.

    Args:
        symbol (str): The stock symbol of the company
        service (GradingSyncService): Injected grading sync service

    Returns:
        GradingRead: The synced grading data

    Raises:
        HTTPException: If grading data is not found for the symbol
    """
    grading = service.upsert_gradings(symbol)
    if not grading:
        raise HTTPException(
            status_code=404, detail=f"Grading data not found for symbol: {symbol}"
        )
    return grading


@router.get(
    "/{symbol}/summary/sync",
    response_model=CompanyGradingSummaryRead,
    summary="Sync company grading summary from external API",
    description="Fetches and upserts a company's grading summary data from the external API into the database.",
)
async def sync_company_grading_summary(
    symbol: str, service: GradingSyncService = Depends(get_grading_sync_service)
):
    """
    Sync a company's grading summary from the external API and store it in the database.

    Args:
        symbol (str): The stock symbol of the company
        service (GradingSyncService): Injected grading sync service

    Returns:
        CompanyGradingSummaryRead: The synced grading summary data

    Raises:
        HTTPException: If grading summary is not found for the symbol
    """
    grading_summary = service.upsert_grading_summary(symbol)
    if not grading_summary:
        raise HTTPException(
            status_code=404, detail=f"Grading summary not found for symbol: {symbol}"
        )
    return grading_summary
