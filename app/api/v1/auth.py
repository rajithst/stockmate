from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db_session
from app.schemas.user import LoginRequest, Token, UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db_session)) -> AuthService:
    """
    Dependency provider for AuthService.
    """
    return AuthService(db)


@router.post("/login", response_model=Token)
def login_for_access_token(
    credentials: Annotated[LoginRequest, Body(embed=False)],
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Authenticate user and return an access token.

    **Request body** - Send as JSON:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

    **Returns:** Access token for authenticated requests
    """
    user = auth_service.authenticate_user(credentials.username, credentials.password)
    return auth_service.create_user_access_token(user)


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    current_user: Annotated[UserRead, Depends(get_current_user)],
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Refresh the access token for the current authenticated user.
    """
    return auth_service.create_user_access_token(current_user)


@router.post("/register", response_model=dict)
def register_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Register a new user.

    Request body:
    {
        "username": "string",
        "email": "user@example.com",
        "password": "string"
    }
    """
    user = auth_service.register_user(
        user_data.username, user_data.password, user_data.email
    )
    return {"success": user.id is not None}


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: Annotated[UserRead, Depends(get_current_user)]):
    """
    Get the current authenticated user.
    """
    return current_user
