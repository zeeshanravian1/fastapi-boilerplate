"""OTP Repository Module.

Description:
- This module contains otp repository.

"""

from fastapi_boilerplate.apps.base.repository import BaseRepository

from .model import OTP, OTPCreate, OTPUpdate


class OTPRepository(BaseRepository[OTP, OTPCreate, OTPUpdate]):
    """OTP Repository Class.

    :Description:
    - This class provides repository for otp.

    """
