"""Authentication Service Module.

Description:
- This module contains authentication service.

"""

from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from jwt import decode

from fastapi_boilerplate.apps.api_v1.user.constant import (
    INACTIVE_USER,
    USER_NOT_FOUND,
)
from fastapi_boilerplate.apps.api_v1.user.helper import UserHelper
from fastapi_boilerplate.apps.api_v1.user.model import (
    User,
    UserCreate,
    UserUpdate,
)
from fastapi_boilerplate.apps.base.model import BaseRead
from fastapi_boilerplate.apps.base.service import BaseService
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.core.security import create_token
from fastapi_boilerplate.database.session import DBSession

from .constant import INCORRECT_PASSWORD, TOKEN_TYPE, TokenType
from .model import LoginResponse, RefreshTokenResponse
from .repository import AuthenticationRepository


class AuthenticationService(BaseService[User, UserCreate, UserUpdate]):
    """Authentication Service Class.

    :Description:
    - This class provides business logic for authentication operations.

    """

    def __init__(self) -> None:
        """Initialize AuthenticationService with AuthenticationRepository."""
        super().__init__(repository=AuthenticationRepository(model=User))
        self.auth_repository: AuthenticationRepository = (
            AuthenticationRepository(model=User)
        )

    def login(
        self,
        db_session: DBSession,
        form_data: OAuth2PasswordRequestForm,
    ) -> LoginResponse | BaseRead[User]:
        """Login User.

        :Description:
        - This method logs in user.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `form_data` (OAuth2PasswordRequestForm): Form data. **(Required)**

        :Returns:
        - `record` (LoginResponse): Login response.

        """
        user: User | None = self.auth_repository.login(
            db_session=db_session, form_data=form_data
        )

        if not user:
            return BaseRead(message=USER_NOT_FOUND)

        if not user.is_active:
            return BaseRead(message=INACTIVE_USER)

        if not UserHelper.verify_password(
            plain_password=form_data.password,
            hashed_password=user.password,
        ):
            return BaseRead(message=INCORRECT_PASSWORD)

        data: dict[str, int | str] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        access_token: str = create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        return LoginResponse(
            token_type=TOKEN_TYPE,
            access_token=access_token,
            refresh_token=refresh_token,
            user=user,
        )

    def refresh_token(
        self,
        db_session: DBSession,
        token: str,
    ) -> RefreshTokenResponse | BaseRead[User]:
        """Refresh Token.

        :Description:
        - This method refreshes authentication token.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `token` (str): Token to refresh. **(Required)**

        :Returns:
        - `record` (RefreshTokenResponse): Login response with new token.

        """
        data: dict[str, int | UUID | float | str | bool] = decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user: User | None = self.auth_repository.read_by_id(
            db_session=db_session,
            record_id=data["id"],  # type: ignore[arg-type]
        )

        if not user:
            return BaseRead(message=USER_NOT_FOUND)

        if not user.is_active:
            return BaseRead(message=INACTIVE_USER)

        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        access_token: str = create_token(
            data=data,  # type: ignore[arg-type]
            token_type=TokenType.ACCESS_TOKEN,
        )

        return RefreshTokenResponse(
            token_type=TOKEN_TYPE,
            access_token=access_token,
        )
