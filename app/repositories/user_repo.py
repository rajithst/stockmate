import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.user import User
from app.schemas.user import UserWrite
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        user = self._get_by_filter(User, {"username": username}, limit=1)
        if user:
            return user[0]
        return None

    def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        user = self._get_by_filter(User, {"email": email}, limit=1)
        if user:
            return user[0]
        return None

    def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID."""
        return self._get_by_id(User, user_id)

    def create_user(self, user_data: UserWrite) -> User:
        """Create a new user."""
        try:
            user = User(**user_data.model_dump(exclude_unset=True))
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error creating user: {e}")
            raise

    def update_user(self, user_id: int, user_data: UserWrite) -> User | None:
        """Update an existing user."""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None

            # Check for duplicate email if changing email
            if user_data.email and user_data.email != user.email:
                if self.get_user_by_email(user_data.email):
                    raise ValueError(f"Email '{user_data.email}' already in use")

            # Update user with provided data
            user = map_model(user, user_data)
            self._db.commit()
            self._db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            raise

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False

            self._db.delete(user)
            self._db.commit()
            return True
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error deleting user {user_id}: {e}")
            raise
