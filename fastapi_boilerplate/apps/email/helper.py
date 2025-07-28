"""Email Helper Module.

Description:
- This module contains all helper functions used by otp package.

"""

import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from jwt import encode
from pydantic import AnyUrl
from pydantic_extra_types.phone_numbers import PhoneNumber

from fastapi_boilerplate.core.config import settings

from .constant import CONTACT_NO_VERIFY_BODY, CONTACT_NO_VERIFY_SUBJECT
from .model import EmailBase, EmailData, SendEmail
from .send_email import send_email
from .send_sms import send_sms


def generate_otp_code() -> str:
    """Generates 6 digit OTP code.

    :Description:
    - This method is used to generate a 6 digit OTP.

    :Args:
    - `None`

    :Returns:
    - `otp_code` (str): 6 digit OTP code.

    """
    return str(secrets.randbelow(10**6)).zfill(6)


async def send_email_otp(user_id: UUID | int, record: EmailBase) -> str:
    """Sends an email with OTP.

    :Description:
    - This method is used to encode OTP code and send it to user via email.

    :Args:
    - `user_id` (UUID | int): Unique identifier for user. **(Required)**
    Email details to be sent with following fields:
    - `subject` (str): Subject of email. **(Required)**
    - `email_purpose` (str): Purpose of email. **(Required)**
    - `user_name` (str): Full name of user. **(Required)**
    - `email` (list[str]): Email of user. **(Required)**

    :Returns:
    - `otp_code` (str): OTP code sent to user.

    """
    # Generate OTP Code
    otp_code: str = generate_otp_code()
    otp_expiry_time: datetime = datetime.now(tz=UTC) + timedelta(
        minutes=settings.EMAIL_RESET_TOKEN_EXPIRE_MINUTES
    )

    # Encode OTP Code
    encoded_jwt: bytes = encode(
        payload={
            "id": user_id,
            "email": record.email,
            "token": otp_code,
            "exp": otp_expiry_time,
        },
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    url: AnyUrl = AnyUrl(
        url="".join(
            [
                settings.FRONTEND_HOST,
                "/",
                record.email_purpose.replace(" ", "-").lower(),
                "/",
                str(encoded_jwt),
            ]
        )
    )

    await send_email(
        email=SendEmail(
            email=[record.email],
            subject=record.subject,
            body=EmailData(
                url=url,
                otp_code=otp_code,
                user_name=record.user_name,
                email_purpose=record.email_purpose,
                company_name=settings.PROJECT_TITLE,
                base_url=settings.FRONTEND_HOST,
            ),
        )
    )

    return otp_code


def send_sms_otp(contact_no: PhoneNumber) -> tuple[str, datetime]:
    """Sends an SMS with OTP.

    :Description:
    - This method is used to send an SMS with OTP to user.

    :Args:
    - `contact_no` (PhoneNumber): Phone number to which the SMS will be sent.
    **(Required)**
    Contact number details to be sent with following fields:
    - `subject` (str): Subject of SMS. **(Required)**
    - `user_name` (str): Full name of user. **(Required)**

    :Returns:
    - `otp_code` (str): OTP code sent to user.
    - `otp_expiry` (datetime): Expiry time of OTP code.

    """
    # Generate OTP Code
    otp_code: str = generate_otp_code()
    otp_expiry_time: datetime = datetime.now(tz=UTC) + timedelta(
        minutes=settings.SMS_RESET_TOKEN_EXPIRE_MINUTES
    )

    send_sms(
        contact_no=contact_no,
        body=CONTACT_NO_VERIFY_SUBJECT
        + "\n"
        + CONTACT_NO_VERIFY_BODY.format(otp_code=otp_code),
    )

    return otp_code, otp_expiry_time
