"""Email Constants.

Description:
- This module contains email constants.

"""

from enum import Enum
from pathlib import Path

from fastapi_boilerplate.core.config import settings

EMAIL_TEMPLATE_FOLDER: Path = Path("static/email")
EMAIL_TEMPLATE_FILE: str = "email.html"

TOKEN: str = "123456"

WELCOME_SUBJECT: str = f"Welcome to {settings.PROJECT_TITLE}"
RESET_PASSWORD_SUBJECT: str = "Reset Password Request"

VERIFICATION_SENT_SUCCESS: str = "Verification code sent successfully"
VERIFICATION_SUCCESS: str = "Verification completed successfully"
ALREADY_VERIFIED: str = "Already verified"
PASSWORD_RESET_SUCCESS: str = "Password reset successfully"

INVALID_OTP: str = "Invalid OTP code, please request a new one"
EXPIRED_OTP: str = "OTP expired"
CONTACT_NO_NOT_FOUND: str = "Contact number not found"
INVALID_REQUEST_TYPE: str = "Invalid request type for this OTP method"

# SMS template
CONTACT_NO_VERIFY_BODY_TEMPLATE: str = f"""
Hi {{user_name}},
Please use following OTP to verify your contact number:

{{otp_code}}

Thanks,
{settings.PROJECT_TITLE} Team
"""


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


class OTPPurpose(str, Enum):
    """OTP Purpose Enum.

    :Description:
    - This enum is used to define OTP purpose.

    """

    EMAIL_VERIFY = "Verify Email"  # nosec B105
    CONTACT_VERIFY = "Verify Contact Number"  # nosec B105
    PASSWORD_RESET = "Reset Password"  # nosec B105
