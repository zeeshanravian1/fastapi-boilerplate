"""User Service.

Description:
- This module contains user service implementation.

"""

from uuid import UUID

from fastapi_boilerplate.apps.base.model import BaseRead
from fastapi_boilerplate.apps.base.service import BaseService
from fastapi_boilerplate.database.session import DBSession

from .constant import (
    INCORRECT_PASSWORD,
    PASSWORD_CHANGE_SUCCESS,
    USER_NOT_FOUND,
)
from .helper import UserHelper
from .model import (
    PasswordChange,
    PasswordChangeRead,
    User,
    UserCreate,
    UserUpdate,
)
from .repository import UserRepository


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """User Service Class.

    :Description:
    - This class provides business logic for user operations.

    """

    def __init__(self) -> None:
        """Initialize UserService with UserRepository."""
        super().__init__(repository=UserRepository(model=User))
        self.user_repository: UserRepository = UserRepository(model=User)

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
        record.password = UserHelper.get_password_hash(
            password=record.password
        )

        return self.user_repository.create(
            db_session=db_session, record=record
        )

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
            record.password = UserHelper.get_password_hash(
                password=record.password
            )

        return self.user_repository.bulk_create(
            db_session=db_session, records=records
        )

    def password_change(
        self,
        db_session: DBSession,
        record_id: UUID | int,
        record: PasswordChange,
    ) -> PasswordChangeRead | BaseRead[User]:
        """Change User Password.

        :Description:
        - This method changes user password.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `record_id` (int): User ID. **(Required)**
        - `record` (PasswordChange): Password change request. **(Required)**

        :Returns:
        - `record` (PasswordChangeRead): Password change response.

        """
        user: User | None = self.user_repository.read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not user:
            return BaseRead(message=USER_NOT_FOUND)

        # Verify old password
        if not UserHelper.verify_password(
            plain_password=record.old_password,
            hashed_password=user.password,
        ):
            return BaseRead(message=INCORRECT_PASSWORD)

        # Update password
        user.password = UserHelper.get_password_hash(
            password=record.new_password
        )

        self.user_repository.update_by_id(
            db_session=db_session,
            record_id=record_id,
            record=user,  # type: ignore[arg-type]
        )

        return PasswordChangeRead(
            message=PASSWORD_CHANGE_SUCCESS,
            data=None,
        )
