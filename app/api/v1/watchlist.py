from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.user import (
    UserRead,
    WatchlistCompanyItem,
    WatchlistItemWrite,
    WatchlistRead,
    WatchlistUpsertRequest,
)
from app.services.watchlist_service import WatchlistService

logger = getLogger(__name__)

router = APIRouter(prefix="")


def get_watchlist_service(
    session: Session = Depends(get_db_session),
) -> WatchlistService:
    return WatchlistService(session=session)


@router.get(
    "/",
    response_model=list[WatchlistRead],
    summary="Get all watchlists for the authenticated user",
)
async def get_watchlists(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchlistService = Depends(get_watchlist_service),
):
    """
    Retrieve all watchlists for the authenticated user.

    Args:
        current_user (UserRead): The authenticated user
        service (WatchlistService): Injected watchlist service
    Returns:
        List[WatchlistRead]: List of user's watchlists
    """
    return service.get_user_watchlists(user_id=current_user.id)


@router.post(
    "/",
    response_model=WatchlistRead,
    summary="Create a new watchlist",
    status_code=status.HTTP_201_CREATED,
)
async def create_watchlist(
    watchlist_in: WatchlistUpsertRequest,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchlistService = Depends(get_watchlist_service),
):
    """
    Create a new watchlist for the authenticated user.

    Args:
        watchlist_in (WatchlistCreate): Watchlist data to create
        current_user (UserRead): The authenticated user
        service (WatchlistService): Injected watchlist service

    Returns:
        WatchlistRead: The created watchlist

    Raises:
        HTTPException: 400 Bad Request if watchlist data is invalid
    """
    try:
        return service.create_watchlist(watchlist_in, user_id=current_user.id)
    except ValueError as e:
        logger.warning(
            f"Failed to create watchlist for user {current_user.id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put(
    "/{watchlist_id}",
    response_model=WatchlistRead,
    summary="Update an existing watchlist",
)
async def update_watchlist(
    watchlist_id: int,
    watchlist_in: WatchlistUpsertRequest,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchlistService = Depends(get_watchlist_service),
):
    """
    Update a watchlist. Only the owner can update their watchlist.

    Args:
        watchlist_id (int): The ID of the watchlist to update
        watchlist_in (WatchlistUpsertRequest): Updated watchlist data
        current_user (UserRead): The authenticated user
        service (WatchlistService): Injected watchlist service

    Returns:
        WatchlistRead: The updated watchlist

    Raises:
        HTTPException: 403 Forbidden if watchlist doesn't exist or user is not the owner
                      400 Bad Request if update data is invalid
    """
    try:
        return service.update_watchlist(
            watchlist_id, watchlist_in, user_id=current_user.id
        )
    except ValueError as e:
        logger.warning(
            f"User {current_user.id} attempted to update watchlist {watchlist_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.delete(
    "/{watchlist_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a watchlist by ID",
)
async def delete_watchlist(
    watchlist_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchlistService = Depends(get_watchlist_service),
):
    """
    Delete a watchlist by its ID. Only the owner can delete their watchlist.

    Args:
        watchlist_id (int): The ID of the watchlist to delete
        current_user (UserRead): The authenticated user
        service (WatchlistService): Injected watchlist service

    Raises:
        HTTPException: 403 Forbidden if watchlist doesn't exist or user is not the owner
    """
    try:
        service.delete_watchlist(watchlist_id, user_id=current_user.id)
        logger.info(f"User {current_user.id} deleted watchlist {watchlist_id}")
    except ValueError as e:
        logger.warning(
            f"User {current_user.id} attempted to delete watchlist {watchlist_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get(
    "/{watchlist_id}",
    response_model=list[WatchlistCompanyItem],
    summary="Get items in a watchlist",
)
async def get_watchlist_items(
    watchlist_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchlistService = Depends(get_watchlist_service),
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
    "/{watchlist_id}/items",
    response_model=WatchlistCompanyItem,
    summary="Add an item to a watchlist",
    status_code=status.HTTP_201_CREATED,
)
async def add_watchlist_item(
    watchlist_id: int,
    watchlist_item_in: WatchlistItemWrite,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchlistService = Depends(get_watchlist_service),
):
    """
    Add a stock symbol to a watchlist. Only the owner can add items to their watchlist.

    Args:
        watchlist_id (int): The ID of the watchlist
        watchlist_item_in (WatchlistItemWrite): The item to add
        current_user (UserRead): The authenticated user
        service (WatchlistService): Injected watchlist service

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
    "/{watchlist_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item from a watchlist",
)
async def delete_watchlist_item(
    watchlist_id: int,
    item_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    service: WatchlistService = Depends(get_watchlist_service),
):
    """
    Delete an item from a watchlist. Only the owner can delete items from their watchlist.

    Args:
        watchlist_id (int): The ID of the watchlist (for RESTful routing)
        item_id (int): The ID of the watchlist item to delete
        current_user (UserRead): The authenticated user
        service (WatchlistService): Injected watchlist service

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
