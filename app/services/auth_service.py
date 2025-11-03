from datetime import timedelta

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.config import config
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserRead, UserWrite


class AuthService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)

    def authenticate_user(self, username: str, password: str) -> User:
        """
        Authenticates a user by username and password.
        If authentication fails, an HTTPException is raised.
        """
        user = self.user_repo.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def register_user(self, username: str, password: str, email: EmailStr) -> User:
        """
        Registers a new user with the given username and password.
        Raises an HTTPException if the username is already taken.
        """
        existing_user = self.user_repo.get_user_by_username(username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        hashed_password = get_password_hash(password)
        user_write = UserWrite(
            username=username, hashed_password=hashed_password, email=email
        )
        user = self.user_repo.create_user(user_write)
        return UserRead.model_validate(user)

    def create_user_access_token(self, user: User) -> dict:
        """
        Creates an access token for a given user.
        """
        access_token_expires = timedelta(minutes=config.auth_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
