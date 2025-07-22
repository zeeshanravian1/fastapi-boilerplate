"""Email Helper Module.

Description:
- This module contains all helper functions used by otp package.

"""

import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from jwt import encode
from pydantic import AnyUrl

from fastapi_boilerplate.core.config import settings

from .model import EmailBase, EmailData, SendEmail
from .send_email import send_email


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
