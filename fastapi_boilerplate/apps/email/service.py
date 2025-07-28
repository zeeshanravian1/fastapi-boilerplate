"""OTP Service Module.

Description:
- This module contains otp service.

"""

from datetime import UTC, datetime

from fastapi import BackgroundTasks
from jwt import decode
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

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
from fastapi_boilerplate.core.security import CurrentUser, create_token
from fastapi_boilerplate.database.session import DBSession

from .constant import (
    CONTACT_NO_SENT_SUCCESS,
    CONTACT_NO_VERIFIED,
    CONTACT_NO_VERIFIED_SUCCESS,
    EMAIL_ALREADY_VERIFIED,
    EMAIL_VERIFY_PURPOSE,
    EMAIL_VERIFY_SUBJECT,
    EXPIRED_OTP,
    INVALID_OTP,
    OTPType,
)
from .helper import send_email_otp, send_sms_otp
from .model import (
    OTP,
    ContactNoVerify,
    ContactNoVerifyRead,
    ContactNoVerifyRequest,
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
            db_session=db_session,
            field=User.email.key,  # type: ignore[attr-defined]
            value=record.email,
        )

        if not user:
            return USER_NOT_FOUND

        if not user.is_active:
            return INACTIVE_USER

        # pylint: disable=no-member
        otp_record: OTP | None = self.otp_repository.read_by_multiple_fields(
            db_session=db_session,
            fields=[
                (OTP.user_id.key, user.id),  # type: ignore[attr-defined]
                (OTP.otp_type.key, OTPType.EMAIL),  # type: ignore
            ],
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

        # pylint: disable=no-member
        otp_record: OTP | None = self.otp_repository.read_by_multiple_fields(
            db_session=db_session,
            fields=[
                (OTP.user_id.key, token_data["id"]),  # type: ignore
                (OTP.otp_type.key, OTPType.EMAIL),  # type: ignore
            ],
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

    async def background_sms(
        self,
        db_session: DBSession,
        user: User,
        otp_record: OTP | None,
        contact_no: PhoneNumber,
    ) -> None:
        """Send SMS in Background Task.

        :Description:
        - This method is used to send SMS in background task.

        :Args:
        - `user` (User): User object containing user details. **(Required)**
        - `otp_record` (OTP | None): OTP record.
        - `contact_no` (str): Contact number to send the OTP. **(Required)**

        :Returns:
        - `None`

        """
        otp_code, otp_expiry = send_sms_otp(contact_no=contact_no)

        if otp_record:
            otp_record.otp = otp_code
            otp_record.otp_expiry = otp_expiry

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
                    otp_type=OTPType.SMS,
                    is_verified=False,
                    otp=otp_code,
                    otp_expiry=otp_expiry,
                ),
            )

    async def verify_contact_no_request(
        self,
        db_session: DBSession,
        record: ContactNoVerifyRequest,
        current_user: CurrentUser,
        background_tasks: BackgroundTasks,
    ) -> str | None:
        """Verify Contact Number Request.

        :Description:
        - This method is used to request contact number verification.

        :Args:
        - `record` (ContactNoBase): Record containing contact number details
        to be verified. **(Required)**

        :Returns:
        - `None`

        """
        user_repository: UserRepository = UserRepository(model=User)

        # pylint: disable=no-member
        user: User | None = user_repository.read_by_multiple_fields(
            db_session=db_session,
            fields=[
                (User.id.key, current_user.id),  # type: ignore[attr-defined]
                (User.contact_no.key, record.contact_no),  # type: ignore
            ],
        )

        if not user:
            return USER_NOT_FOUND

        if not user.is_active:
            return INACTIVE_USER

        # pylint: disable=no-member
        otp_record: OTP | None = self.otp_repository.read_by_multiple_fields(
            db_session=db_session,
            fields=[
                (OTP.user_id.key, user.id),  # type: ignore[attr-defined]
                (OTP.otp_type.key, OTPType.SMS),  # type: ignore
            ],
        )

        if otp_record and otp_record.is_verified:
            return CONTACT_NO_VERIFIED

        # Send SMS in Background Task
        background_tasks.add_task(
            self.background_sms,
            db_session=db_session,
            user=user,
            otp_record=otp_record,
            contact_no=record.contact_no,
        )

        return CONTACT_NO_SENT_SUCCESS

    def verify_contact_no(
        self,
        db_session: DBSession,
        record: ContactNoVerify,
        current_user: CurrentUser,
    ) -> ContactNoVerifyRead:
        """Verify Contact Number.

        :Description:
        - This method is used to verify contact number.

        :Args:
        - `record` (ContactNoVerify): Record containing token to be verified.
        **(Required)**

        :Returns:
        - `ContactNoVerifyRead`: Response containing verification status and
        data.

        """
        # pylint: disable=no-member
        otp_record: OTP | None = self.otp_repository.read_by_multiple_fields(
            db_session=db_session,
            fields=[
                (OTP.user_id.key, current_user.id),  # type: ignore
                (OTP.otp_type.key, OTPType.SMS),  # type: ignore
            ],
        )

        if not otp_record or otp_record.otp != record.otp:
            return ContactNoVerifyRead(message=INVALID_OTP)

        if otp_record.is_verified:
            return ContactNoVerifyRead(message=CONTACT_NO_VERIFIED)

        if otp_record.otp_expiry and otp_record.otp_expiry < datetime.now(
            tz=UTC
        ):
            return ContactNoVerifyRead(message=EXPIRED_OTP)

        otp_record.is_verified = True
        otp_record.otp_expiry = None

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
            return ContactNoVerifyRead(message=USER_NOT_FOUND)

        if not user.is_active:
            return ContactNoVerifyRead(message=INACTIVE_USER)

        return ContactNoVerifyRead(message=CONTACT_NO_VERIFIED_SUCCESS)
