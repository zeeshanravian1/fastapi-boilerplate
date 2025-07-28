"""Send Email Module.

Description:
- This module is used to send email to user.

"""

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from fastapi_boilerplate.core.config import settings

from .constant import EMAIL_TEMPLATE_FILE, EMAIL_TEMPLATE_FOLDER
from .model import SendEmail

# Email Configuration
email_config: ConnectionConfig = ConnectionConfig(
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_USERNAME=settings.SMTP_USER,  # type: ignore[arg-type]
    MAIL_FROM=settings.SMTP_EMAIL,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
    MAIL_STARTTLS=settings.SMTP_TLS,
    MAIL_SSL_TLS=settings.SMTP_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=EMAIL_TEMPLATE_FOLDER,
)


# Sending OTP Code
async def send_email(email: SendEmail) -> None:
    """Sends email to user.

    :Description:
    - This method is used to send an email to user.

    :Args:
    - `email` (SendEmail): Email data to be sent. **(Required)**

    :Returns:
    - `None`

    """
    message: MessageSchema = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=email.body.model_dump(),
        subtype=MessageType.html,
    )

    fastapi_mail: FastMail = FastMail(config=email_config)

    await fastapi_mail.send_message(
        message=message, template_name=EMAIL_TEMPLATE_FILE
    )
