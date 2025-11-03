from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.user import UserRead
from app.schemas.watchlist import (
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
        watchlist_in (WatchlistWrite): Updated watchlist data
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
