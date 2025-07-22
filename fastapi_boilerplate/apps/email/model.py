"""Email Model.

Description:
- This module contains email models.

"""

from pydantic import AnyUrl, EmailStr, field_validator
from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig

from fastapi_boilerplate.apps.api_v1.user.helper import validate_email
from fastapi_boilerplate.apps.auth.model import LoginResponse
from fastapi_boilerplate.apps.base.model import BaseRead
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.database.connection import Base

from .constant import (
    EMAIL_SENT_SUCCESS,
    EMAIL_VERIFIED_SUCCESS,
    EMAIL_VERIFY_PURPOSE,
    OTPType,
)


class OTPBase(SQLModel):
    """OTP Base Model.

    :Description:
    - This class contains base model for OTP.

    :Attributes:
    - `otp_type` (OTPType): Type of OTP (email, sms, password).
    - `otp` (str): One Time Password.
    - `is_verified` (bool): Status of OTP verification.
    - `user_id` (UUID | int): Unique identifier for user.

    """

    otp_type: OTPType = Field(
        min_length=1,
        max_length=50,
        schema_extra={"examples": OTPType.choices()},
    )
    otp: str = Field(
        min_length=6,
        max_length=6,
        schema_extra={"examples": ["123456"]},
    )
    is_verified: bool = Field(
        default=False,
        schema_extra={"examples": [True]},
    )
    user_id: int = Field(
        foreign_key="user.id",
        schema_extra={"examples": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class OTP(Base, OTPBase, table=True):
    """OTP Table.

    :Description:
    - This class contains model for OTP table.

    :Attributes:
    - `id` (UUID | int): Unique identifier for OTP.
    - `otp_type` (OTPType): Type of OTP (email, sms, password).
    - `otp` (str): One Time Password.
    - `user_id` (UUID | int): Unique identifier for user.
    - `created_at` (datetime): Timestamp when OTP was created.
    - `updated_at` (datetime): Timestamp when OTP was last updated.

    """


class OTPCreate(OTPBase):
    """OTP Create Model.

    :Description:
    - This class contains model for creating OTP.

    :Attributes:
    - `otp_type` (OTPType): Type of OTP (email, sms, password).
    - `otp` (str): One Time Password.
    - `is_verified` (bool): Status of OTP verification.
    - `user_id` (UUID | int): Unique identifier for user.

    """


class OTPUpdate(OTPBase):
    """OTP Update Model.

    :Description:
    - This class contains model for updating OTP.

    :Attributes:
    - `otp_type` (OTPType): Type of OTP (email, sms, password).
    - `otp` (str): One Time Password.
    - `is_verified` (bool): Status of OTP verification.
    - `user_id` (UUID | int): Unique identifier for user.

    """


class EmailBase(SQLModel):
    """Email Base Model.

    Description:
    - This model is used to validate base email data passed to send email.

    :Attributes:
    - `subject` (str): Subject of email.
    - `email_purpose` (str): Purpose of email.
    - `user_name` (str): Name of user to be included in email
    - `email` (EmailStr): Email address to send email.

    """

    subject: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [EMAIL_VERIFY_PURPOSE]},
    )
    email_purpose: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [EMAIL_VERIFY_PURPOSE]},
    )
    user_name: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["John Doe"]},
    )
    email: EmailStr = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["johndoe@example.com"]},
    )

    # Custom Validators
    email_validator = field_validator("email")(validate_email)

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class EmailData(SQLModel):
    """Email Data Model.

    :Description:
    - This model is used to validate email data passed to send email.

    :Attributes:
    - `url` (AnyUrl): URL to be included in email.
    - `otp_code` (str): OTP code to be included in email.
    - `user_name` (str): Name of user to be included in email
    - `email_purpose` (str): Purpose of email.
    - `company_name` (str): Name of company to be included in email
    - `base_url` (str): Base URL for application.

    """

    url: AnyUrl = Field(
        schema_extra={"examples": [settings.FRONTEND_HOST]},
    )
    otp_code: str = Field(
        min_length=6,
        max_length=6,
        schema_extra={"examples": ["123456"]},
    )
    user_name: str = Field(
        schema_extra={"examples": ["John Doe"]},
    )
    email_purpose: str = Field(
        schema_extra={"examples": [EMAIL_VERIFY_PURPOSE]},
    )
    company_name: str = Field(
        schema_extra={"examples": [settings.PROJECT_TITLE]},
    )
    base_url: str = Field(
        schema_extra={"examples": [settings.FRONTEND_HOST]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class SendEmail(SQLModel):
    """Send Email Model.

    :Description:
    - This model is used to validate email data passed to send email.

    :Attributes:
    - `email` (list[EmailStr]): List of email addresses to send email.
    - `subject` (str): Subject of email.
    - `body` (EmailData): Body of email.

    """

    email: list[EmailStr] = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["john@example.com"]},
    )
    subject: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [EMAIL_VERIFY_PURPOSE]},
    )
    body: EmailData

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class EmailVerifyRequest(SQLModel):
    """Email Verify Request Model.

    :Description:
    - This class contains model for request email verify

    :Attributes:
    - `email` (EmailStr | None): Email of user.

    """

    email: EmailStr = Field(
        unique=True, schema_extra={"examples": ["johndoe@example.com"]}
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    email_validator = field_validator("email")(validate_email)


class EmailVerifyRequestRead(BaseRead[OTP]):
    """Email Verify Response Model.

    :Description:
    - This class contains model for response email verify

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (None): No data returned.
    - `error` (str | None): Error message if any.

    """

    message: str = Field(
        default=EMAIL_SENT_SUCCESS,
        schema_extra={"examples": [EMAIL_SENT_SUCCESS]},
    )
    data: None = Field(default=None)  # type: ignore[unused-ignore]


class EmailVerify(SQLModel):
    """Email Verify Model.

    :Description:
    - This class contains model for email verification.

    :Attributes:
    - `token` (str): Token for email verification.

    """

    token: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["token_value"]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class EmailVerifyRead(BaseRead[LoginResponse]):
    """Email Verify Response Model.

    :Description:
    - This class contains model for response email verify

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (LoginResponse | None): Data containing user login information.
    - `error` (str | None): Error message if any.

    """

    message: str = Field(
        default=EMAIL_VERIFIED_SUCCESS,
        schema_extra={"examples": [EMAIL_VERIFIED_SUCCESS]},
    )
    data: LoginResponse | None = Field(default=None)
