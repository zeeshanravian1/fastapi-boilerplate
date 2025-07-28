"""Send SMS Module.

Description:
- This module is used to send SMS to user.

"""

from pydantic_extra_types.phone_numbers import PhoneNumber
from twilio.rest import Client

from fastapi_boilerplate.core.config import settings


def send_sms(contact_no: PhoneNumber, body: str) -> None:
    """Sends SMS to user.

    :Description:
    - This method is used to send an SMS to user.

    :Args:
    - `contact_no` (PhoneNumber): Phone number to which the SMS will be sent.
    **(Required)**
    - `body` (str): Content of the SMS to be sent. **(Required)**

    :Returns:
    - `None`

    """
    client: Client = Client(
        username=settings.TWILIO_ACCOUNT_SID,
        password=settings.TWILIO_AUTH_TOKEN,
    )

    client.messages.create(  # type: ignore[no-untyped-call]
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=contact_no,
    )
