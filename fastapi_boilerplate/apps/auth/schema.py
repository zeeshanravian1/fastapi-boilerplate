"""
Authentication Pydantic Schemas

Description:
- This module contains all auth schemas used by API.

"""

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from ...apps.api_v1.user.schema import UserReadSchema
from ...core.configuration import TokenType
from .configuration import auth_configuration


class LoginReadSchema(UserReadSchema):
    """
    Login Read Schema

    Description:
    - This schema is used to validate login data returned by API.

    """

    token_type: str = Field(examples=[auth_configuration.TOKEN_TYPE])
    access_token: str = Field(examples=[TokenType.ACCESS_TOKEN])
    refresh_token: str = Field(examples=[TokenType.REFRESH_TOKEN])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RefreshToken(BaseModel):
    """
    Refresh Token Schema

    Description:
    - This schema is used to validate refresh token passed to API.

    """

    refresh_token: str = Field(examples=[TokenType.REFRESH_TOKEN])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RefreshTokenReadSchema(BaseModel):
    """
    Refresh Token Read Schema

    Description:
    - This schema is used to validate refresh token data returned by API.

    """

    token_type: str = Field(examples=[auth_configuration.TOKEN_TYPE])
    access_token: str = Field(examples=[TokenType.ACCESS_TOKEN])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
