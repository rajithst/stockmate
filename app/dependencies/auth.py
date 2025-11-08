from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
import jwt
from sqlalchemy.orm import Session

from app.core.config import config
from app.dependencies.db import get_db_session
from app.repositories.user_repo import UserRepository
from app.schemas.user import TokenData
from app.schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db_session)
) -> UserRead:
    """
    Decode the JWT token to get the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.auth_secret_key, algorithms=[config.auth_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserRead.model_validate(user)
