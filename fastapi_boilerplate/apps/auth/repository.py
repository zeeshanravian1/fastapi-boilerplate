"""Authentication Repository Module.

Description:
- This module contains authentication repository.

"""

from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import col, or_, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from fastapi_boilerplate.apps.api_v1.user.model import (
    User,
    UserCreate,
    UserUpdate,
)
from fastapi_boilerplate.apps.base.repository import BaseRepository
from fastapi_boilerplate.database.session import DBSession


class AuthenticationRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Authentication Repository Class.

    :Description:
    - This class provides repository for authentication.

    """

    def login(
        self,
        db_session: DBSession,
        form_data: OAuth2PasswordRequestForm,
    ) -> User | None:
        """Login User.

        :Description:
        - This method logs in user.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `form_data` (OAuth2PasswordRequestForm): Form data. **(Required)**

        :Returns:
        - `record` (User | None): User record.

        """
        query: SelectOfScalar[User] = select(User).where(
            or_(
                col(column_expression=User.email) == form_data.username,
                col(column_expression=User.username) == form_data.username,
            ),
        )

        return db_session.exec(statement=query).one_or_none()
