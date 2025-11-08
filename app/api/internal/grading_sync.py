from fastapi import APIRouter, Depends, HTTPException

from app.api.internal.config import ERROR_MESSAGES, TAGS
from app.dependencies.sync_services import create_sync_service_provider
from app.schemas.market_data import CompanyGradingRead, CompanyGradingSummaryRead
from app.services.internal.grading_sync_service import GradingSyncService

router = APIRouter(prefix="", tags=[TAGS["grading"]["name"]])

# Create dependency provider for GradingSyncService
get_grading_sync_service = create_sync_service_provider(GradingSyncService)


@router.get(
    "/{symbol}/sync",
    response_model=list[CompanyGradingRead],
    summary="Sync company gradings from external API",
    description="Fetches and upserts a company's grading data from the external API into the database.",
)
def sync_gradings(
    symbol: str, service: GradingSyncService = Depends(get_grading_sync_service)
):
    """Sync a company's grading data from the external API and store it in the database."""
    grading = service.upsert_gradings(symbol)
    if not grading:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_GRADINGS"].format(symbol=symbol),
        )
    return grading


@router.get(
    "/{symbol}/summary/sync",
    response_model=CompanyGradingSummaryRead,
    summary="Sync company grading summary from external API",
    description="Fetches and upserts a company's grading summary data from the external API into the database.",
)
def sync_grading_summary(
    symbol: str, service: GradingSyncService = Depends(get_grading_sync_service)
):
    """Sync a company's grading summary from the external API and store it in the database."""
    grading_summary = service.upsert_grading_summary(symbol)
    if not grading_summary:
        raise HTTPException(
            status_code=404,
            detail=ERROR_MESSAGES["NOT_FOUND_GRADINGS"].format(symbol=symbol),
        )
    return grading_summary
