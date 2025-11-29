from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.user import DashboardResponse, UserRead, StockSymbol
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="")


def get_dashboard_service(
    session=Depends(get_db_session),
) -> DashboardService:
    return DashboardService(session=session)


@router.get("/", response_model=DashboardResponse, summary="Get dashboard data")
def get_dashboard_data(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: DashboardService = Depends(get_dashboard_service),
):
    """
    Retrieve dashboard summary data for the authenticated user.
    """
    return service.get_dashboard_summary(user_id=current_user.id)


@router.get(
    "/symbols", response_model=list[StockSymbol], summary="Get all stock symbols"
)
def get_all_stock_symbols(
    service: DashboardService = Depends(get_dashboard_service),
):
    """
    Retrieve a list of all stock symbols available in the system.
    """
    return service.get_all_stock_symbols()
