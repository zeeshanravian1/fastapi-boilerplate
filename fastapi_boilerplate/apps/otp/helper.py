"""Email Helper Module.

Description:
- This module contains all helper functions used by otp package.

"""

import secrets
from datetime import UTC, datetime, timedelta

from jwt import encode
from pydantic import AnyUrl

from fastapi_boilerplate.core.config import settings

from .model import EmailBase, EmailData, SendEmail, SendSMS
from .send_email import send_email
from .send_sms import send_sms


class OTPSender:
    """OTP Sender class for handling email and SMS OTP operations."""

    def generate_otp_code(self) -> str:
        """Generates 6 digit OTP code.

        :Description:
        - This method is used to generate a 6 digit OTP.

        :Args:
        - `None`

        :Returns:
        - `otp_code` (str): 6 digit OTP code.

        """
        return str(secrets.randbelow(exclusive_upper_bound=10**6)).zfill(6)

    async def send_otp(
        self, record: EmailBase | SendSMS
    ) -> tuple[str, datetime]:
        """Sends OTP via email or SMS.

        :Description:
        - This method is used to send OTP code via email or SMS.

        :Args:
        - `user_id` (UUID | int): Unique identifier for user. **(Optional)**
        - `record` (EmailBase | SendSMS): Record containing details for sending
        OTP. **(Required)**

        :Returns:
        - `data` (tuple[str, datetime | None]): OTP code and expiry time.

        """
        otp_code: str = self.generate_otp_code()

        otp_expiry_time: datetime = datetime.now(tz=UTC) + timedelta(
            minutes=(
                settings.SMS_RESET_TOKEN_EXPIRE_MINUTES
                if isinstance(record, SendSMS)
                else settings.EMAIL_RESET_TOKEN_EXPIRE_MINUTES
            )
        )

        if isinstance(record, EmailBase):
            encoded_jwt: bytes = encode(
                payload={
                    "id": record.user_id,
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
                        email_purpose=record.email_purpose,
                        otp_code=otp_code,
                        user_name=record.user_name,
                        company_name=settings.PROJECT_TITLE,
                    ),
                )
            )

        else:
            send_sms(sms=record)

        return otp_code, otp_expiry_time
