"""
User Pydantic Schemas

Description:
- This module contains all user schemas used by API.

"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_settings import SettingsConfigDict

from fastapi_boilerplate.apps.base.schema import (
    BasePaginationReadSchema,
    BaseReadSchema,
)

from ..role.schema import RoleReadSchema
from .configuration import user_configuration
from .helper import lowercase_email, password_validator, username_validator
from .response_message import user_response_message


class UserBaseSchema(BaseModel):
    """
    User Base Schema

    Description:
    - This schema is used to validate user base data passed to API.

    """

    name: str | None = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.NAME],
    )
    username: str | None = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.USERNAME],
    )
    email: EmailStr | None = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.EMAIL],
    )
    role_id: int | None = Field(
        ge=1,
        examples=[user_configuration.ROLE_ID],
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class UserCreateSchema(UserBaseSchema):
    """
    User create Schema

    Description:
    - This schema is used to validate user creation data passed to API.

    """

    name: str = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.NAME],
    )
    username: str = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.USERNAME],
    )
    email: EmailStr = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.EMAIL],
    )
    password: str = Field(
        min_length=8,
        max_length=1_00,
        examples=[user_configuration.PASSWORD],
    )
    role_id: int = Field(
        ge=1,
        examples=[user_configuration.ROLE_ID],
    )

    # Custom Validators
    username_validator = field_validator("username")(username_validator)
    email_validator = field_validator("email")(lowercase_email)
    password_validator = field_validator("password")(password_validator)


class UserReadSchema(UserBaseSchema, BaseReadSchema):
    """
    User Read Schema

    Description:
    - This schema is used to validate user data returned by API.

    """


class UserRoleReadSchema(UserBaseSchema, BaseReadSchema):
    """
    User Role Read Schema

    Description:
    - This schema is used to validate user role data returned by API.

    """

    role_details: RoleReadSchema


class UserRolePaginationReadSchema(BasePaginationReadSchema):
    """
    User Role Pagination Read Schema

    Description:
    - This schema is used to validate user role pagination data returned by
    API.

    """

    records: list[UserRoleReadSchema]


class UserPaginationReadSchema(BasePaginationReadSchema):
    """
    User Pagination Read Schema

    Description:
    - This schema is used to validate user pagination data returned by API.

    """

    records: list[UserReadSchema]


class UserUpdateSchema(UserBaseSchema):
    """
    User Update Schema

    Description:
    - This schema is used to validate user update data passed to API.

    """

    name: str = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.NAME],
    )
    username: str = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.USERNAME],
    )
    email: EmailStr = Field(
        min_length=1,
        max_length=2_55,
        examples=[user_configuration.EMAIL],
    )
    role_id: int = Field(
        ge=1,
        examples=[user_configuration.ROLE_ID],
    )


class UserPartialUpdateSchema(UserBaseSchema):
    """
    User Update Schema

    Description:
    - This schema is used to validate user update data passed to API.

    """

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=1_00,
        examples=[user_configuration.PASSWORD],
    )


class PasswordChangeSchema(BaseModel):
    """
    Change Password Schema

    Description:
    - This schema is used to validate change password data passed to API.

    """

    old_password: str = Field(
        min_length=8, max_length=1_00, examples=[user_configuration.PASSWORD]
    )
    new_password: str = Field(
        min_length=8, max_length=1_00, examples=[user_configuration.PASSWORD]
    )

    # Custom Validators
    old_password_validator = field_validator("old_password")(
        password_validator
    )
    new_password_validator = field_validator("new_password")(
        password_validator
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class PasswordChangeReadSchema(BaseModel):
    """
    Change Password Read Schema

    Description:
    - This schema is used to validate change password data returned by API.

    """

    detail: str = Field(examples=[user_response_message.PASSWORD_CHANGED])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
