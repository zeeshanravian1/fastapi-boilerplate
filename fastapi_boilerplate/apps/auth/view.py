"""
Authentication View Module

Description:
- This module is responsible for auth views.

"""

from typing import Any, Type

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Result, or_, select
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.selectable import Select

from fastapi_boilerplate.core.configuration import (
    TokenType,
    core_configuration,
)
from fastapi_boilerplate.core.security import create_token

from ...apps.api_v1.user.model import UserTable
from ...apps.api_v1.user.schema import UserCreateSchema, UserUpdateSchema
from ...apps.base.view import BaseView
from .configuration import auth_configuration
from .response_message import auth_response_message
from .schema import LoginReadSchema, RefreshToken, RefreshTokenReadSchema


# Authentication class
class AuthView(
    BaseView[
        UserTable,
        UserCreateSchema,
        UserUpdateSchema,
    ]
):
    """
    Authentication View Class

    Description:
    - This class is responsible for auth views.

    """

    def __init__(
        self,
        model: Type[UserTable],
    ) -> None:
        """
        Authentication View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (UserTable): User Database Model.

        """

        super().__init__(model=model)

    async def login(
        self, db_session: Session, form_data: OAuth2PasswordRequestForm
    ) -> LoginReadSchema | dict[str, str]:
        """
        Login.

        Description:
        - This method is responsible for login user.

        Parameter:
        - **email or username** (STR): Email or username of user.
        **(Required)**
        - **password** (STR): Password of user. **(Required)**

        Return:
        - **token_type** (STR): Token type of user.
        - **access_token** (STR): Access token of user.
        - **refresh_token** (STR): Refresh token of user.

        """

        form_data.username = form_data.username.lower()

        query: Select[tuple[UserTable]] = select(UserTable).where(
            or_(
                UserTable.username == form_data.username,
                UserTable.email == form_data.username,
            )
        )
        result: Result[tuple[UserTable]] = db_session.execute(statement=query)
        user_data: UserTable | None = result.scalars().first()

        if not user_data:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        if not pbkdf2_sha256.verify(form_data.password, user_data.password):
            return {"detail": auth_response_message.INCORRECT_PASSWORD}

        data: dict[str, Any] = {
            "id": user_data.id,
            "username": user_data.username,
            "email": user_data.email,
        }

        access_token: str = create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        return LoginReadSchema(
            id=user_data.id,
            name=user_data.name,
            username=user_data.username,
            email=user_data.email,
            role_id=user_data.role_id,
            created_at=user_data.created_at,
            updated_at=user_data.updated_at,
            token_type=auth_configuration.TOKEN_TYPE,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_token(
        self, db_session: Session, record: RefreshToken
    ) -> RefreshTokenReadSchema | dict[str, str]:
        """
        Refresh Token.

        Description:
        - This method is responsible for refresh token.

        Parameter:
        - **record** (STR): Refresh token of user. **(Required)**

        Return:
        - **token_type** (STR): Token type of user.
        - **access_token** (STR): Access token of user.

        """

        data: dict[str, Any] = jwt.decode(
            token=record.refresh_token,
            key=core_configuration.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[core_configuration.ALGORITHM],
        )

        result: UserTable | None = await super().read_by_id(
            db_session=db_session,
            record_id=data.get("id"),  # type: ignore
        )

        if not result:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        return RefreshTokenReadSchema(
            token_type=TokenType.ACCESS_TOKEN,
            access_token=create_token(
                data=data, token_type=TokenType.ACCESS_TOKEN
            ),
        )


auth_view = AuthView(model=UserTable)
