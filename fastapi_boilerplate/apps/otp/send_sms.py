"""Send SMS Module.

Description:
- This module is used to send SMS to user.

"""

from twilio.rest import Client

from fastapi_boilerplate.core.config import settings

from .model import SendSMS


def send_sms(sms: SendSMS) -> None:
    """Sends SMS to user.

    :Description:
    - This method is used to send an SMS to user.

    :Args:
    - `contact_no` (PhoneNumber): Phone number to which SMS will be sent.
    **(Required)**
    - `body` (str): Content of SMS to be sent. **(Required)**

    :Returns:
    - `None`

    """
    client: Client = Client(
        username=settings.TWILIO_ACCOUNT_SID,
        password=settings.TWILIO_AUTH_TOKEN,
    )

    client.messages.create(  # type: ignore[no-untyped-call]
        from_=settings.TWILIO_PHONE_NUMBER,
        to=sms.contact_no,
        body=sms.subject + "\n" + sms.body,
    )
