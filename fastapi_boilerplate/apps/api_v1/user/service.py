"""User Service.

Description:
- This module contains user service implementation.

"""

from fastapi_boilerplate.apps.base.service import BaseService
from fastapi_boilerplate.database.session import DBSession

from .helper import get_password_hash
from .model import User, UserCreate, UserUpdate
from .repository import UserRepository


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """User Service Class.

    :Description:
    - This class provides business logic for user operations.

    """

    def __init__(self) -> None:
        """Initialize UserService with UserRepository."""
        super().__init__(repository=UserRepository(model=User))

    def create(self, db_session: DBSession, record: UserCreate) -> User:
        """Create a new user.

        :Description:
        - This method creates a new user in database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record` (UserCreate): User object to be added to database.
        **(Required)**

        :Returns:
        - `record` (User): Created user.

        """
        # Hash password before saving
        record.password = get_password_hash(password=record.password)

        return super().create(db_session=db_session, record=record)

    def bulk_create(
        self, db_session: DBSession, records: list[UserCreate]
    ) -> list[User]:
        """Create multiple users.

        :Description:
        - This method creates multiple users in database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[UserCreate]): List of Model objects to be added to
        database. **(Required)**

        :Returns:
        - `records` (list[User]): List of created records.

        """
        # Hash passwords before saving
        for record in records:
            record.password = get_password_hash(password=record.password)

        return super().bulk_create(db_session=db_session, records=records)
