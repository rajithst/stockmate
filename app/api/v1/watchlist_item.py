from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.user import UserRead
from app.schemas.user import (
    WatchlistCompanyItem,
    WatchlistItemWrite,
)
from app.services.watchlist_service import WatchListItemService

router = APIRouter(prefix="/{watchlist_id}/items")


def get_watchlist_item_service(
    session: Session = Depends(get_db_session),
) -> WatchListItemService:
    return WatchListItemService(session=session)


@router.get(
    "",
    response_model=List[WatchlistCompanyItem],
    summary="Get items in a watchlist",
)
async def get_watchlist_items(
    watchlist_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchListItemService = Depends(get_watchlist_item_service),
):
    """
    Retrieve all items in a specific watchlist. Only the owner can access their watchlist items.

    Args:
        watchlist_id (int): The ID of the watchlist
        current_user (UserRead): The authenticated user
        service (WatchListItemService): Injected watchlist item service

    Returns:
        List[WatchlistCompanyItem]: List of watchlist items with company details
    """
    try:
        return service.get_watchlist_items(watchlist_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.post(
    "",
    response_model=WatchlistCompanyItem,
    summary="Add an item to a watchlist",
    status_code=status.HTTP_201_CREATED,
)
async def add_watchlist_item(
    watchlist_id: int,
    watchlist_item_in: WatchlistItemWrite,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchListItemService = Depends(get_watchlist_item_service),
):
    """
    Add a stock symbol to a watchlist. Only the owner can add items to their watchlist.

    Args:
        watchlist_id (int): The ID of the watchlist
        watchlist_item_in (WatchlistItemWrite): The item to add
        current_user (UserRead): The authenticated user
        service (WatchListItemService): Injected watchlist item service

    Returns:
        WatchlistCompanyItem: The added watchlist item with company details
    """
    try:
        return service.add_watchlist_item(
            watchlist_id, watchlist_item_in, user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item from a watchlist",
)
async def delete_watchlist_item(
    watchlist_id: int,
    item_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchListItemService = Depends(get_watchlist_item_service),
):
    """
    Delete an item from a watchlist. Only the owner can delete items from their watchlist.

    Args:
        watchlist_id (int): The ID of the watchlist (for RESTful routing)
        item_id (int): The ID of the watchlist item to delete
        current_user (UserRead): The authenticated user
        service (WatchListItemService): Injected watchlist item service

    Returns:
        None
    """
    try:
        service.delete_watchlist_item(watchlist_id, item_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
