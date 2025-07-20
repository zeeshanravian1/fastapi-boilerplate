"""Token, Scopes, and Security Management Module.

Description:
- This module is used to create a token for user and get current user.

"""

from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, decode, encode
from pydantic import ValidationError

from fastapi_boilerplate.apps.api_v1.user.model import User, UserResponse
from fastapi_boilerplate.apps.auth.constant import TOKEN_TYPE, TokenType
from fastapi_boilerplate.database.session import DBSession

from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


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
    to_encode: dict[str, int | str | datetime] = data.copy()  # type: ignore

    expire_minutes: int = (
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
        if token_type == TokenType.ACCESS_TOKEN
        else settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    expire: datetime = datetime.now(tz=UTC) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})

    return str(
        encode(
            payload=to_encode,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
    )


def get_current_user(
    db_session: DBSession,
    access_token: str = Depends(dependency=oauth2_scheme),
) -> UserResponse:
    """Get current user.

    :Description:
    - This function is used to get current user.

    :Args:
    - `db_session` (DBSession): Database session. **(Required)**
    - `access_token` (str): Encoded token to get current user. **(Required)**

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
        payload: dict[str, Any] = decode(
            jwt=access_token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id: int | None = payload.get("id")
        user_name: str | None = payload.get("username")
        user_email: str | None = payload.get("email")

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

    return UserResponse.model_validate(obj=user)


def get_current_active_user(
    current_user: UserResponse = Security(dependency=get_current_user),
) -> UserResponse:
    """Get current active user.

    :Description:
    - This function is used to get current active user.

    :Args:
    - `current_user` (UserResponse): Current user details. **(Required)**

    :Returns:
    - **user** (UserResponse): User details.

    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return UserResponse.model_validate(obj=current_user)


CurrentUser = Annotated[User, Depends(dependency=get_current_active_user)]
