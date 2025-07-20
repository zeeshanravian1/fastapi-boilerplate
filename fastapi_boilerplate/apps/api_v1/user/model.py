"""User Model.

Description:
- This module contains user model and schemas.

"""

from collections.abc import Sequence

from pydantic import EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig

from fastapi_boilerplate.apps.base.model import (
    BaseBulkUpdate,
    BasePaginationData,
    BasePaginationRead,
    BaseRead,
)
from fastapi_boilerplate.database.connection import Base


class UserBase(SQLModel):
    """User Base Model.

    :Description:
    - This class contains base model for user table.

    :Attributes:
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """

    first_name: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["John"]},
    )
    last_name: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["Doe"]},
    )
    contact_no: PhoneNumber | None = Field(
        default=None,
        min_length=1,
        max_length=20,
        schema_extra={"examples": ["+1 417-555-1234"]},
    )
    username: str = Field(
        min_length=1,
        max_length=255,
        unique=True,
        regex=r"^[a-zA-Z0-9_.-]+$",
        schema_extra={"examples": ["johndoe"]},
    )
    email: EmailStr = Field(
        unique=True, schema_extra={"examples": ["johndoe@example.com"]}
    )
    address: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["123 Main St, Springfield"]},
    )
    city: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["Springfield"]},
    )
    state: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["IL"]},
    )
    country: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["USA"]},
    )
    postal_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
        regex=r"^\d{5}(-\d{4})?$",
        schema_extra={"examples": ["62701", "62701-1234"]},
    )
    profile_image_path: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["path/to/profile/image.jpg"]},
    )
    is_active: bool | None = Field(
        default=True,
        schema_extra={"examples": [True]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    @field_validator("contact_no", mode="after")
    @classmethod
    def validate_contact_no(cls, value: str | None) -> str | None:
        """Validate contact number to remove 'tel:' prefix."""
        if value is None:
            return value

        return str(value).replace("tel:", "")


class User(Base, UserBase, table=True):
    """User Table.

    :Description:
    - This class contains model for user table.

    :Attributes:
    - `id` (UUID | int): Unique identifier for user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `password` (str): Password of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.
    - `created_at` (datetime): Timestamp when user was created.
    - `updated_at` (datetime): Timestamp when user was last updated.

    """

    password: str = Field(
        min_length=8,
        max_length=255,
        schema_extra={"examples": ["12345@Aa"]},
    )


class UserCreate(UserBase):
    """User Create Model.

    :Description:
    - This class contains model for creating user.

    :Attributes:
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `password` (str): Password of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """

    password: str = Field(
        min_length=8,
        max_length=255,
        schema_extra={"examples": ["12345@Aa"]},
    )


class UserResponse(Base, UserBase):
    """User Response Model.

    :Description:
    - This class contains model for user response.

    :Attributes:
    - `id` (UUID | int): Unique identifier for user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.
    - `created_at` (datetime): Timestamp when user was created.
    - `updated_at` (datetime): Timestamp when user was last updated.

    """


class UserRead(BaseRead[UserResponse]):
    """User Read Model.

    :Description:
    - This class contains model for reading user.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (UserResponse | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: UserResponse | None = Field(default=None)


class UserBulkRead(BaseRead[UserResponse]):
    """User Bulk Read Model.

    :Description:
    - This class contains model for reading multiple users.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (list[UserResponse]): List of users.
    - `error` (str | None): Error message if any.

    """

    data: list[UserResponse]  # type: ignore[assignment]


class UserPaginationData(BasePaginationData[UserResponse]):
    """User Pagination Data Model.

    :Description:
    - This class contains model for paginated reading of users.

    :Attributes:
    - `page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `records` (Sequence[UserResponse]): List of user records for current
    page.

    """

    records: Sequence[UserResponse]


class UserPaginationRead(BasePaginationRead[UserResponse]):
    """User Pagination Read Model.

    :Description:
    - This class contains model for paginated reading of users.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (BasePaginationData[UserResponse]): Paginated data for response.
    - `error` (str | None): Error message if any.

    """

    data: UserPaginationData  # type: ignore[unused-ignore]


class UserUpdate(UserBase):
    """User Update Model.

    :Description:
    - This class contains model for updating user.

    :Attributes:
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """


class UserBulkUpdate(BaseBulkUpdate, UserUpdate):
    """User Bulk Update Model.

    :Description:
    - This class contains model for bulk updating users.

    :Attributes:
    - `data` (list[UserUpdate]): List of users to be updated.
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `error` (str | None): Error message if any.

    """


class UserPatch(UserBase):
    """User Patch Model.

    :Description:
    - This class contains model for patching user.

    :Attributes:
    - `first_name` (str | None): First name of user.
    - `last_name` (str | None): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str | None): Username of user.
    - `email` (str | None): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool | None): Status of user account.

    """

    first_name: str | None = Field(  # type: ignore[assignment]
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["John"]},
    )
    last_name: str | None = Field(  # type: ignore[assignment]
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["Doe"]},
    )
    username: str | None = Field(  # type: ignore[assignment]
        default=None,
        min_length=1,
        max_length=255,
        unique=True,
        regex=r"^[a-zA-Z0-9_.-]+$",
        schema_extra={"examples": ["johndoe"]},
    )
    email: EmailStr | None = Field(  # type: ignore[assignment]
        default=None,
        schema_extra={"examples": ["johndoe@example.com"]},
    )


class UserBulkPatch(BaseBulkUpdate, UserPatch):
    """User Bulk Patch Model.

    :Description:
    - This class contains model for bulk patching users.

    :Attributes:
    - `data` (list[UserPatch]): List of users to be patched.
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `error` (str | None): Error message if any.

    """
