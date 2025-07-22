"""OTP Service Module.

Description:
- This module contains otp service.

"""

from datetime import datetime

from fastapi import BackgroundTasks
from jwt import decode
from pydantic import EmailStr

from fastapi_boilerplate.apps.api_v1.user.constant import (
    INACTIVE_USER,
    USER_NOT_FOUND,
)
from fastapi_boilerplate.apps.api_v1.user.model import User
from fastapi_boilerplate.apps.api_v1.user.repository import UserRepository
from fastapi_boilerplate.apps.auth.constant import TOKEN_TYPE, TokenType
from fastapi_boilerplate.apps.auth.model import LoginResponse
from fastapi_boilerplate.apps.base.service import BaseService
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.core.security import create_token
from fastapi_boilerplate.database.session import DBSession

from .constant import (
    EMAIL_ALREADY_VERIFIED,
    EMAIL_VERIFY_PURPOSE,
    EMAIL_VERIFY_SUBJECT,
    INVALID_OTP,
    OTPType,
)
from .helper import send_email_otp
from .model import (
    OTP,
    EmailBase,
    EmailVerify,
    EmailVerifyRead,
    EmailVerifyRequest,
    OTPCreate,
    OTPUpdate,
)
from .repository import OTPRepository


class OTPService(BaseService[OTP, OTPCreate, OTPUpdate]):
    """OTP Service Class.

    :Description:
    - This class provides business logic for otp operations.

    """

    def __init__(self) -> None:
        """Initialize OTPService with OTPRepository."""
        super().__init__(repository=OTPRepository(model=OTP))
        self.otp_repository = OTPRepository(model=OTP)

    async def background_email(
        self,
        db_session: DBSession,
        user: User,
        otp_record: OTP | None,
        email: EmailStr,
    ) -> None:
        """Send Email in Background Task.

        :Description:
        - This method is used to send email in background task.

        :Args:
        - `user` (User): User object containing user details. **(Required)**
        - `otp_record` (OTP | None): OTP record.
        - `email` (EmailStr): Email address to send the OTP. **(Required)**

        :Returns:
        - `None`

        """
        otp_code: str = await send_email_otp(
            user_id=user.id,
            record=EmailBase(
                subject=EMAIL_VERIFY_SUBJECT,
                email_purpose=EMAIL_VERIFY_PURPOSE,
                user_name=f"{user.first_name} {user.last_name}",
                email=email,
            ),
        )

        if otp_record:
            otp_record.otp = otp_code

            self.otp_repository.update_by_id(
                db_session=db_session,
                record_id=otp_record.id,
                record=OTPUpdate(**otp_record.model_dump()),
            )

        else:
            self.otp_repository.create(
                db_session=db_session,
                record=OTPCreate(
                    user_id=user.id,
                    otp_type=OTPType.EMAIL,
                    is_verified=False,
                    otp=otp_code,
                ),
            )

    async def verify_email_request(
        self,
        db_session: DBSession,
        record: EmailVerifyRequest,
        background_tasks: BackgroundTasks,
    ) -> str | None:
        """Verify Email Request.

        :Description:
        - This method is used to request email verification.

        :Args:
        - `record` (EmailStr): Record containing email details to be verified.
        **(Required)**

        :Returns:
        - `None`

        """
        user_repository: UserRepository = UserRepository(model=User)

        user: User | None = user_repository.read_by_field(
            db_session=db_session, field="email", value=record.email
        )

        if not user:
            return USER_NOT_FOUND

        if not user.is_active:
            return INACTIVE_USER

        otp_record: OTP | None = self.otp_repository.read_by_field(
            db_session=db_session,
            field=OTP.user_id.key,  # type: ignore[attr-defined]
            value=user.id,
        )

        if otp_record and otp_record.is_verified:
            return EMAIL_ALREADY_VERIFIED

        # Send Email in Background Task
        background_tasks.add_task(
            self.background_email,
            db_session=db_session,
            user=user,
            otp_record=otp_record,
            email=record.email,
        )

        return None

    def verify_email(
        self, db_session: DBSession, record: EmailVerify
    ) -> EmailVerifyRead:
        """Verify Email.

        :Description:
        - This method is used to verify email.

        :Args:
        - `record` (EmailVerify): Record containing token to be verified.
        **(Required)**

        :Returns:


        """
        token_data: dict[str, str | datetime] = decode(
            jwt=record.token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        otp_record: OTP | None = self.otp_repository.read_by_field(
            db_session=db_session,
            field=OTP.user_id.key,  # type: ignore[attr-defined]
            value=token_data["id"],
        )

        if not otp_record or otp_record.otp != token_data["token"]:
            return EmailVerifyRead(message=INVALID_OTP)

        if otp_record.is_verified:
            return EmailVerifyRead(message=EMAIL_ALREADY_VERIFIED)

        otp_record.is_verified = True

        self.otp_repository.update_by_id(
            db_session=db_session,
            record_id=otp_record.id,
            record=OTPUpdate(**otp_record.model_dump()),
        )

        user_repository: UserRepository = UserRepository(model=User)

        user: User | None = user_repository.read_by_id(
            db_session=db_session, record_id=otp_record.user_id
        )

        if not user:
            return EmailVerifyRead(message=USER_NOT_FOUND)

        if not user.is_active:
            return EmailVerifyRead(message=INACTIVE_USER)

        data: dict[str, int | str] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        access_token: str = create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        return EmailVerifyRead(
            message=EMAIL_VERIFY_PURPOSE,
            data=LoginResponse(
                token_type=TOKEN_TYPE,
                access_token=access_token,
                refresh_token=refresh_token,
            ),
        )
