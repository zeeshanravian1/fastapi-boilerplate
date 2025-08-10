"""Email Model.

Description:
- This module contains email models.

"""

from datetime import UTC, datetime

from pydantic import AnyUrl, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import DateTime, Field, SQLModel
from sqlmodel._compat import SQLModelConfig

from fastapi_boilerplate.apps.api_v1.user.helper import (
    validate_contact,
    validate_email,
)
from fastapi_boilerplate.apps.auth.model import LoginResponse
from fastapi_boilerplate.apps.base.model import BaseRead
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.database.connection import Base

from .constant import (
    CONTACT_NO_SENT_SUCCESS,
    CONTACT_NO_VERIFIED_SUCCESS,
    CONTACT_NO_VERIFY_SUBJECT,
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
    otp_expiry: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        schema_extra={"examples": [datetime.now(tz=UTC)]},
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

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    email_validator = field_validator("email")(validate_email)


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


class ContactNoBase(SQLModel):
    """Contact No Base Model.

    Description:
    - This model is used to validate base contact number data passed to send
    SMS.

    :Attributes:
    - `subject` (str): Subject of SMS.
    - `sms_purpose` (str): Purpose of SMS.
    - `user_name` (str): Name of user to be included in SMS.
    - `contact_no` (PhoneNumber): Phone number to send SMS.

    """

    subject: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [CONTACT_NO_VERIFY_SUBJECT]},
    )
    sms_purpose: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["Verify Contact Number"]},
    )
    user_name: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["John Doe"]},
    )
    contact_no: PhoneNumber | None = Field(
        default=None,
        schema_extra={"examples": ["+1 417-555-1234"]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    contact_no_validator = field_validator("contact_no")(validate_contact)


class ContactNoData(SQLModel):
    """Contact No Data Model.

    :Description:
    - This model is used to validate contact number data passed to send SMS.

    :Attributes:
    - `otp_code` (str): OTP code to be included in SMS.
    - `user_name` (str): Name of user to be included in SMS.
    - `sms_purpose` (str): Purpose of SMS.
    - `company_name` (str): Name of company to be included in SMS.

    """

    otp_code: str = Field(
        min_length=6,
        max_length=6,
        schema_extra={"examples": ["123456"]},
    )
    user_name: str = Field(
        schema_extra={"examples": ["John Doe"]},
    )
    sms_purpose: str = Field(
        schema_extra={"examples": ["Verify Contact Number"]},
    )
    company_name: str = Field(
        schema_extra={"examples": [settings.PROJECT_TITLE]},
    )


class SendContactNoSMS(SQLModel):
    """Send Contact No SMS Model.

    :Description:
    - This model is used to validate contact number data passed to send SMS.

    :Attributes:
    - `contact_no` (PhoneNumber): Phone number to send SMS.
    - `subject` (str): Subject of SMS.
    - `body` (ContactNoData): Body of SMS.

    """

    contact_no: PhoneNumber = Field(
        schema_extra={"examples": ["+1 417-555-1234"]},
    )
    subject: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [CONTACT_NO_VERIFY_SUBJECT]},
    )
    body: ContactNoData

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    contact_no_validator = field_validator("contact_no")(validate_contact)


class ContactNoVerifyRequest(SQLModel):
    """Contact No Verify Request Model.

    :Description:
    - This class contains model for request contact number verify

    :Attributes:
    - `contact_no` (PhoneNumber | None): Contact number of user.

    """

    contact_no: PhoneNumber = Field(
        unique=True, schema_extra={"examples": ["+1 417-555-1234"]}
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    contact_no_validator = field_validator("contact_no")(validate_contact)


class ContactNoVerifyRequestRead(BaseRead[OTP]):
    """Contact No Verify Response Model.

    :Description:
    - This class contains model for response contact number verify

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (None): No data returned.
    - `error` (str | None): Error message if any.

    """

    message: str = Field(
        default=CONTACT_NO_SENT_SUCCESS,
        schema_extra={"examples": [CONTACT_NO_SENT_SUCCESS]},
    )
    data: None = Field(default=None)  # type: ignore[unused-ignore]


class ContactNoVerify(SQLModel):
    """Contact No Verify Model.

    :Description:
    - This class contains model for contact number verification.

    :Attributes:
    - `otp` (str): OTP for contact number verification.

    """

    otp: str = Field(
        min_length=6,
        max_length=6,
        schema_extra={"examples": ["123456"]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class ContactNoVerifyRead(BaseRead[OTP]):
    """Contact No Verify Response Model.

    :Description:
    - This class contains model for response contact number verify

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (LoginResponse | None): Data containing user login information.
    - `error` (str | None): Error message if any.

    """

    message: str = Field(
        default=CONTACT_NO_VERIFIED_SUCCESS,
        schema_extra={"examples": [CONTACT_NO_VERIFIED_SUCCESS]},
    )
    data: None = Field(default=None)  # type: ignore[unused-ignore]


class PasswordResetRequest(SQLModel):
    """Password Reset Request Model.

    :Description:
    - This class contains model for request password reset

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


class PasswordResetRequestRead(BaseRead[OTP]):
    """Password Reset Response Model.

    :Description:
    - This class contains model for response password reset request

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


class PasswordReset(SQLModel):
    """Password Reset Model.

    :Description:
    - This class contains model for password reset.

    :Attributes:
    - `token` (str): Token for password reset.
    - `new_password` (str): New password for user.

    """

    token: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["token_value"]},
    )
    new_password: str = Field(
        min_length=8,
        max_length=128,
        schema_extra={"examples": ["12345@Aa"]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class PasswordResetRead(BaseRead[LoginResponse]):
    """Password Reset Response Model.

    :Description:
    - This class contains model for response password reset

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
