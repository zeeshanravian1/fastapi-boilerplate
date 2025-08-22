"""Token, Scopes, and Security Management Module.

Description:
- This module is used to create a token for user and get current user.

"""

from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, decode, encode
from pydantic import ValidationError

from fastapi_boilerplate.apps.api_v1.user.model import User
from fastapi_boilerplate.apps.auth.constant import TOKEN_TYPE, TokenType
from fastapi_boilerplate.database.session import DBSession

from .config import settings


class SecurityManager:
    """Security Manager Class.

    :Description:
    - This class is used to manage security-related operations.

    """

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

    @staticmethod
    def create_token(data: dict[str, int | str], token_type: TokenType) -> str:
        """Create token.

        :Description:
        - This function is used to create access token and refresh token.

        :Args:
        - `data` (JSON): Data to be encoded in token. **(Required)**
        - `token_type` (TokenType): Type of token to be created. **(Required)**
            - **Allowed values:** "access_token", "refresh_token"

        :Returns:
        - `token` (STR): Created token.

        """
        to_encode: dict[str, int | str] = data.copy()

        to_encode["exp"] = datetime.now(UTC) + timedelta(  # type: ignore
            minutes=(
                settings.ACCESS_TOKEN_EXPIRE_MINUTES
                if token_type == TokenType.ACCESS_TOKEN
                else settings.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        )

        return str(
            encode(
                payload=to_encode,
                key=settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
            )
        )

    @staticmethod
    def get_current_user(
        db_session: DBSession,
        access_token: str = Depends(dependency=oauth2_scheme),
    ) -> User:
        """Get current user.

        :Description:
        - This function is used to get current user.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `access_token` (str): Encoded token to get current user.
        **(Required)**

        :Returns:
        - **user** (UserRead): User details.

        """
        authenticate_value: str = TOKEN_TYPE

        credentials_exception: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        try:
            payload: dict[str, int | UUID | float | str | bool] = decode(
                jwt=access_token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            user_id: int | None = payload.get("id")  # type: ignore[assignment]
            user_name: str | None = payload.get("username")  # type: ignore
            user_email: str | None = payload.get("email")  # type: ignore

            if user_name is None or user_email is None:
                raise credentials_exception

        except (InvalidTokenError, ValidationError) as err:
            raise credentials_exception from err

        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while getting current user",
            ) from err

        user: User | None = db_session.get(entity=User, ident=user_id)

        if not user:
            raise credentials_exception

        return user

    @staticmethod
    def get_current_active_user(
        current_user: User = Security(dependency=get_current_user),
    ) -> User:
        """Get current active user.

        :Description:
        - This function is used to get current active user.

        :Args:
        - `current_user` (User): Current user details. **(Required)**

        :Returns:
        - **user** (User): User details.

        """
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )

        return current_user


CurrentUser = Annotated[
    User, Depends(dependency=SecurityManager.get_current_active_user)
]
