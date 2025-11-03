from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.portfolio import PortfolioRead, PortfolioWrite
from app.schemas.user import UserRead
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="")


def get_portfolio_service(
    session: Session = Depends(get_db_session),
) -> PortfolioService:
    return PortfolioService(session=session)


@router.get("/", response_model=List[PortfolioRead], summary="Get all portfolios")
async def get_portfolios(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: PortfolioService = Depends(get_portfolio_service),
):
    """
    Retrieve all portfolios for the authenticated user.

    Args:
        current_user (UserRead): The authenticated user
        service (PortfolioService): Injected portfolio service

    Returns:
        List[PortfolioRead]: List of user's portfolios
    """
    return service.get_all_portfolios(user_id=current_user.id)


@router.post(
    "/",
    response_model=PortfolioRead,
    summary="Create a new portfolio",
    status_code=status.HTTP_201_CREATED,
)
async def create_portfolio(
    portfolio_in: PortfolioWrite,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: PortfolioService = Depends(get_portfolio_service),
):
    """
    Create a new portfolio for the authenticated user.

    Args:
        portfolio_in (PortfolioWrite): Portfolio data to create
        current_user (UserRead): The authenticated user
        service (PortfolioService): Injected portfolio service
    """
    return service.create_portfolio(portfolio_in, user_id=current_user.id)


@router.put(
    "/",
    response_model=PortfolioRead,
    summary="Update a portfolio",
    status_code=status.HTTP_200_OK,
)
async def update_portfolio(
    portfolio_in: PortfolioWrite,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: PortfolioService = Depends(get_portfolio_service),
):
    """
    Create or update a portfolio for the authenticated user.
    Args:
        portfolio_in (PortfolioWrite): Portfolio data to create or update
        current_user (UserRead): The authenticated user
        service (PortfolioService): Injected portfolio service

    Returns:
        PortfolioRead: The created portfolio
    """
    return service.update_portfolio(portfolio_in, user_id=current_user.id)


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a portfolio by ID",
)
async def delete_portfolio(
    portfolio_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: PortfolioService = Depends(get_portfolio_service),
):
    """
    Delete a portfolio by its ID. Only the owner can delete their portfolio.

    Args:
        portfolio_id (int): The ID of the portfolio to delete
        current_user (UserRead): The authenticated user
        service (PortfolioService): Injected portfolio service

    Returns:
        None
    """
    service.delete_portfolio(portfolio_id, user_id=current_user.id)
