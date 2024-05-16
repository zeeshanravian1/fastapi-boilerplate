"""
Token, Scopes, and Security

Description:
- This module is used to create a token for user and get current user.

"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.engine.result import Result
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from fastapi_boilerplate.apps.api_v1.user.model import UserTable
from fastapi_boilerplate.core.configuration import core_configuration
from fastapi_boilerplate.database.session import get_session

from .configuration import TokenType
from .schema import CurrentUserReadSchema

security_logger: logging.Logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_token(data: dict, token_type: TokenType) -> str:
    """
    Create token

    Description:
    - This function is used to create access token and refresh token.

    Parameter:
    - **data** (JSON): Data to be encoded in token. **(Required)**
    - **token_type** (TokenType): Type of token to be created. **(Required)**
        - **Allowed values:** "access_token", "refresh_token"

    Return:
    - **token** (STR): Created token.

    """

    to_encode: dict = data.copy()

    expire_minutes: int = (
        core_configuration.ACCESS_TOKEN_EXPIRE_MINUTES
        if token_type == TokenType.ACCESS_TOKEN
        else core_configuration.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    secret_key: str = (
        core_configuration.ACCESS_TOKEN_SECRET_KEY
        if token_type == TokenType.ACCESS_TOKEN
        else core_configuration.REFRESH_TOKEN_SECRET_KEY
    )

    expire: datetime = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expire_minutes
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        claims=to_encode,
        key=secret_key,
        algorithm=core_configuration.ALGORITHM,
    )


async def get_current_user(
    security_scopes: SecurityScopes,
    db_session: Session = Depends(get_session),
    access_token: str = Depends(oauth2_scheme),
) -> CurrentUserReadSchema:
    """
    Get current user.

    Description:
    - This function is used to get current user.

    Parameter:
    - **db_session** (AsyncSession): Database session. **(Required)**
    - **token** (STR): Encoded token to get current user. **(Required)**

    Return:
    - **user** (CurrentUserReadSchema): User details.

    """

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value: str = "Bearer"  # type: ignore
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            token=access_token,
            key=core_configuration.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[core_configuration.ALGORITHM],
        )

        user_id: str = payload.get("id")  # type: ignore
        user_name: str = payload.get("username")  # type: ignore
        user_email: str = payload.get("email")  # type: ignore

        if user_name is None or user_email is None:
            raise credentials_exception

    except (JWTError, ValidationError) as err:
        raise credentials_exception from err

    except Exception as err:
        security_logger.exception(msg=err)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while getting current user",
        ) from err

    query: Select = select(UserTable).where(UserTable.id == user_id)
    result: Result[Any] = db_session.execute(statement=query)
    user_data: UserTable | None = result.scalars().first()

    if not user_data:
        raise credentials_exception

    current_user: dict = {
        "id": user_data.id,
        "name": user_data.name,
        "username": user_data.username,
        "email": user_data.email,
        "role_id": user_data.role_id,
        "role_name": user_data.role.role_name,
        "created_at": user_data.created_at,
        "updated_at": user_data.updated_at,
    }

    if user_data.role.role_name == core_configuration.SUPERUSER_ROLE:
        return CurrentUserReadSchema.model_validate(obj=current_user)

    return CurrentUserReadSchema(**current_user)


async def get_current_active_user(
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> CurrentUserReadSchema:
    """
    Get current active user.

    Description:
    - This function is used to get current active user.

    Parameter:
    - **current_user** (CurrentUserReadSchema): Current user details.
    **(Required)**

    Return:
    - **user** (CurrentUserReadSchema): User details.

    """

    return CurrentUserReadSchema.model_validate(obj=current_user)
