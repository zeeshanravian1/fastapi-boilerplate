"""Blog Model.

Description:
- This module contains blog models.

"""

from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig

from fastapi_boilerplate.apps.base.model import BaseRead

from .constant import TOKEN_TYPE, TokenType


class LoginResponse(SQLModel):
    """Login Response Model.

    :Description:
    - This class contains model for login response.

    :Attributes:
    - `token_type` (str): Type of token.
    - `access_token` (str): Access token.
    - `refresh_token` (str): Refresh token.

    """

    token_type: str = Field(
        min_items=1,
        max_items=255,
        schema_extra={"examples": [TOKEN_TYPE]},
    )
    access_token: str = Field(
        min_items=1,
        schema_extra={"examples": [TokenType.ACCESS_TOKEN]},
    )
    refresh_token: str = Field(
        min_items=1,
        schema_extra={"examples": [TokenType.REFRESH_TOKEN]},
    )

    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class LoginRead(BaseRead[LoginResponse]):
    """Login Read.

    :Description:
    - This class contains model for returning login data.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (LoginResponse | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: LoginResponse | None = Field(default=None)


class RefreshToken(SQLModel):
    """Refresh Token Model.

    :Description:
    - This class is used to validate refresh token passed to API.

    """

    refresh_token: str = Field(
        schema_extra={"examples": [TokenType.REFRESH_TOKEN]},
    )

    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class RefreshTokenResponse(SQLModel):
    """Refresh Token Response Model.

    :Description:
    - This class contains model for refresh token response.

    :Attributes:
    - `token_type` (str): Type of token.
    - `access_token` (str): Access token.

    """

    token_type: str = Field(
        min_items=1,
        max_items=255,
        schema_extra={"examples": ["Bearer"]},
    )
    access_token: str = Field(
        min_items=1,
        schema_extra={"examples": [TokenType.ACCESS_TOKEN]},
    )

    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class RefreshTokenRead(BaseRead[RefreshTokenResponse]):
    """Refresh Token Read Model.

    :Description:
    - This class contains model for refresh token read.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (RefreshTokenResponse | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: RefreshTokenResponse | None = Field(default=None)
