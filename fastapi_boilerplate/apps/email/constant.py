"""Email Constants.

Description:
- This module contains email constants.

"""

from enum import Enum
from pathlib import Path

from fastapi_boilerplate.core.config import settings

EMAIL_TEMPLATE_FOLDER: Path = Path("static/email")
EMAIL_TEMPLATE_FILE: str = "email.html"

EMAIL_VERIFY_SUBJECT: str = f"Welcome to {settings.PROJECT_TITLE}"
EMAIL_VERIFY_PURPOSE: str = "Verify Email"

EMAIL_ALREADY_VERIFIED: str = "Email already verified"
EMAIL_SENT_SUCCESS: str = "Email sent successfully"
EMAIL_VERIFIED_SUCCESS: str = "Email verified successfully"

CONTACT_NO_VERIFY_SUBJECT: str = f"Welcome to {settings.PROJECT_TITLE}"
CONTACT_NO_VERIFY_PURPOSE: str = "Verify Contact Number"
CONTACT_NO_VERIFY_BODY: str = f"""
Hi,
Please use the following OTP to verify your contact number:

{{otp_code}}

Thanks,
The {settings.PROJECT_TITLE} Team
"""

CONTACT_NO_VERIFIED: str = "Contact number already verified"
CONTACT_NO_SENT_SUCCESS: str = "OTP sent successfully"
CONTACT_NO_VERIFIED_SUCCESS: str = "Contact number verified successfully"

PASSWORD_RESET_SUBJECT: str = "Reset Password Request"
PASSWORD_RESET_PURPOSE: str = "Reset Password"
PASSWORD_CHANGE_SUCCESS: str = "Password changed successfully"

INVALID_OTP: str = "Invalid OTP code, please request a new one"
EXPIRED_OTP: str = "OTP expired"


class OTPType(str, Enum):
    """OTP Type Enum.

    :Description:
    - This enum is used to define OTP type.

    """

    EMAIL = "email"  # nosec B105
    SMS = "sms"  # nosec B105
    PASSWORD = "password"  # nosec B105

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """Choices Method.

        :Description:
        - This method is used to get choices for enum.

        :Args:
        - `None`

        :Returns:
        - `choices` (list[tuple[str, str]]): List of choices for enum.

        """
        return [(key.value, key.name) for key in cls]
