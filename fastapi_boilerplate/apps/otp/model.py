"""Email Model.

Description:
- This module contains email models.

"""

from datetime import UTC, datetime
from uuid import UUID

from pydantic import AnyUrl, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import DateTime, Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from fastapi_boilerplate.apps.api_v1.user.constant import (
    CONTACT_NO,
    EMAIL,
    NAME,
    PASSWORD,
)
from fastapi_boilerplate.apps.api_v1.user.helper import (
    validate_contact,
    validate_email,
)
from fastapi_boilerplate.apps.api_v1.user.model import User
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.database.connection import Base

from .constant import (
    CONTACT_NO_VERIFY_BODY_TEMPLATE,
    TOKEN,
    WELCOME_SUBJECT,
    OTPPurpose,
    OTPType,
)


class OTPBase(SQLModel):
    """OTP Base Model.

    :Description:
    - This class contains base model for OTP.

    :Attributes:
    - `otp_type` (OTPType): Type of OTP (email, sms, password).
    - `otp` (str): One Time Password.
    - `otp_expiry` (datetime | None): Expiry time of OTP.
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
        schema_extra={"examples": [TOKEN]},
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
    - `otp_expiry` (datetime | None): Expiry time of OTP.
    - `user_id` (UUID | int): Unique identifier for user.
    - `created_at` (datetime): Timestamp when OTP was created.
    - `updated_at` (datetime): Timestamp when OTP was last updated.

    """

    user: User = Relationship(back_populates="otps")


class OTPCreate(OTPBase):
    """OTP Create Model.

    :Description:
    - This class contains model for creating OTP.

    :Attributes:
    - `otp_type` (OTPType): Type of OTP (email, sms, password).
    - `otp` (str): One Time Password.
    - `otp_expiry` (datetime | None): Expiry time of OTP.
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
    - `otp_expiry` (datetime | None): Expiry time of OTP.
    - `is_verified` (bool): Status of OTP verification.
    - `user_id` (UUID | int): Unique identifier for user.

    """


class EmailBase(SQLModel):
    """Email Base Model.

    :Description:
    - This model is used to validate base email data passed to send email.

    :Attributes:
    - `user_id` (UUID | int): Unique identifier for user.
    - `user_name` (str): Name of user to be included in email.
    - `email` (EmailStr): Email address to send email.
    - `subject` (str): Subject of email.
    - `email_purpose` (str): Purpose of email.

    """

    user_id: UUID | int = Field(
        schema_extra={"examples": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]},
    )
    user_name: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [NAME]},
    )
    email: EmailStr = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [EMAIL]},
    )
    subject: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [WELCOME_SUBJECT]},
    )
    email_purpose: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [OTPPurpose.EMAIL_VERIFY.value]},
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
    - `email_purpose` (str): Purpose of email.
    - `otp_code` (str): OTP code to be included in email.
    - `user_name` (str): Name of user to be included in email
    - `company_name` (str): Name of company to be included in email

    """

    url: AnyUrl = Field(
        schema_extra={"examples": [settings.FRONTEND_HOST]},
    )
    email_purpose: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [OTPPurpose.EMAIL_VERIFY.value]},
    )
    otp_code: str = Field(
        min_length=6,
        max_length=6,
        schema_extra={"examples": [TOKEN]},
    )
    user_name: str = Field(
        schema_extra={"examples": [NAME]},
    )
    company_name: str = Field(
        schema_extra={"examples": [settings.PROJECT_TITLE]},
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
        schema_extra={"examples": [EMAIL]},
    )
    subject: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [WELCOME_SUBJECT]},
    )
    body: EmailData

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class SendSMS(SQLModel):
    """Send SMS Base Model.

    :Description:
    - This model is used to validate sms data passed to send sms.

    :Attributes:
    - `contact_no` (PhoneNumber): Phone number to send SMS.
    - `subject` (str): Subject of SMS.
    - `body` (str): Body of SMS.

    """

    contact_no: PhoneNumber | None = Field(
        default=None,
        schema_extra={"examples": [CONTACT_NO]},
    )
    subject: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": [WELCOME_SUBJECT]},
    )
    body: str = Field(
        schema_extra={"examples": [CONTACT_NO_VERIFY_BODY_TEMPLATE]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    contact_no_validator = field_validator("contact_no")(validate_contact)


class EmailVerifyRequest(SQLModel):
    """Email Verify Request Model.

    :Description:
    - This class contains model for request email verify

    :Attributes:
    - `email` (EmailStr | None): Email of user.

    """

    email: EmailStr = Field(schema_extra={"examples": [EMAIL]})

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    email_validator = field_validator("email")(validate_email)


class ContactNoVerifyRequest(SQLModel):
    """Contact No Verify Request Model.

    :Description:
    - This class contains model for request contact number verify

    :Attributes:
    - `contact_no` (PhoneNumber | None): Contact number of user.

    """

    contact_no: PhoneNumber = Field(
        unique=True, schema_extra={"examples": [CONTACT_NO]}
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    contact_no_validator = field_validator("contact_no")(validate_contact)


class PasswordResetRequest(SQLModel):
    """Password Reset Request Model.

    :Description:
    - This class contains model for request password reset

    :Attributes:
    - `email` (EmailStr | None): Email of user.

    """

    email: EmailStr = Field(schema_extra={"examples": [EMAIL]})

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )

    # Custom Validators
    email_validator = field_validator("email")(validate_email)


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
        schema_extra={"examples": [TOKEN]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class ContactNoVerify(SQLModel):
    """Contact No Verify Model.

    :Description:
    - This class contains model for contact number verification.

    :Attributes:
    - `token` (str): Token for contact number verification.

    """

    token: str = Field(
        min_length=6,
        max_length=6,
        schema_extra={"examples": [TOKEN]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


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
        schema_extra={"examples": [TOKEN]},
    )
    new_password: str = Field(
        min_length=8,
        max_length=128,
        schema_extra={"examples": [PASSWORD]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )
