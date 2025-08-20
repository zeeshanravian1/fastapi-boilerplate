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
from fastapi_boilerplate.apps.api_v1.user.helper import UserHelper
from fastapi_boilerplate.apps.api_v1.user.model import User, UserUpdate
from fastapi_boilerplate.apps.api_v1.user.repository import UserRepository
from fastapi_boilerplate.apps.auth.constant import TOKEN_TYPE, TokenType
from fastapi_boilerplate.apps.auth.model import LoginResponse
from fastapi_boilerplate.apps.base.model import BaseRead
from fastapi_boilerplate.apps.base.service import BaseService
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.core.security import CurrentUser, create_token
from fastapi_boilerplate.database.session import DBSession

from .constant import (
    ALREADY_VERIFIED,
    CONTACT_NO_NOT_FOUND,
    CONTACT_NO_VERIFY_BODY_TEMPLATE,
    EXPIRED_OTP,
    INVALID_OTP,
    INVALID_REQUEST_TYPE,
    RESET_PASSWORD_SUBJECT,
    VERIFICATION_SENT_SUCCESS,
    VERIFICATION_SUCCESS,
    WELCOME_SUBJECT,
    OTPPurpose,
    OTPType,
)
from .helper import OTPSender
from .model import (
    OTP,
    ContactNoVerify,
    ContactNoVerifyRequest,
    EmailBase,
    EmailVerify,
    EmailVerifyRequest,
    OTPCreate,
    OTPUpdate,
    PasswordReset,
    PasswordResetRequest,
    SendSMS,
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
        self.otp_repository: OTPRepository = OTPRepository(model=OTP)
        self.user_repository: UserRepository = UserRepository(model=User)
        self.otp_sender: OTPSender = OTPSender()

    async def send_otp_background(
        self,
        db_session: DBSession,
        user: User,
        otp_record: OTP | None,
        otp_type: OTPType,
        contact_info: EmailStr | PhoneNumber,
    ) -> None:
        """Send OTP in Background Task.

        :Description:
        - This method sends OTP via email or SMS in background task.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `user` (User): User object containing user details. **(Required)**
        - `otp_record` (OTP | None): Existing OTP record if any.
        - `otp_type` (OTPType): Type of OTP (EMAIL, SMS, PASSWORD).
        **(Required)**
        - `contact_info` (EmailStr | PhoneNumber): Email or phone number.
        **(Required)**

        :Returns:
        - `None`

        """
        otp_code: str
        otp_expiry: datetime | None

        if otp_type == OTPType.SMS:
            otp_code, otp_expiry = await self.otp_sender.send_otp(
                record=SendSMS(
                    contact_no=contact_info,  # type:ignore[unused-ignore]
                    subject=WELCOME_SUBJECT,
                    body=CONTACT_NO_VERIFY_BODY_TEMPLATE,
                    user_name=f"{user.first_name} {user.last_name}",
                )
            )

        else:
            email_purpose: str = (
                OTPPurpose.EMAIL_VERIFY.value
                if otp_type == OTPType.EMAIL
                else OTPPurpose.PASSWORD_RESET.value
            )
            email_subject: str = (
                WELCOME_SUBJECT
                if otp_type == OTPType.EMAIL
                else RESET_PASSWORD_SUBJECT
            )

            otp_code, otp_expiry = await self.otp_sender.send_otp(
                record=EmailBase(
                    user_id=user.id,
                    user_name=f"{user.first_name} {user.last_name}",
                    email=contact_info,
                    subject=email_subject,
                    email_purpose=email_purpose,
                ),
            )

            otp_expiry = None

        if otp_record:
            otp_record.otp = otp_code

            if otp_type == OTPType.SMS:
                otp_record.otp_expiry = otp_expiry

            self.otp_repository.update_by_id(
                db_session=db_session,
                record_id=otp_record.id,
                record=OTPUpdate(**otp_record.model_dump()),
            )

        else:
            otp_data: OTPCreate = OTPCreate(
                otp_type=otp_type,
                otp=otp_code,
                otp_expiry=otp_expiry,
                user_id=user.id,
            )

            self.otp_repository.create(
                db_session=db_session,
                record=otp_data,
            )

    async def request_otp(
        self,
        db_session: DBSession,
        otp_type: OTPType,
        background_tasks: BackgroundTasks,
        record: (
            EmailVerifyRequest | ContactNoVerifyRequest | PasswordResetRequest
        ),
        current_user: CurrentUser | None = None,
    ) -> BaseRead[OTP]:
        """Request OTP for verification.

        :Description:
        - This method handles OTP requests for email, SMS, or password reset.

        :Args:
        RequestOTPParams with following fields:
        - `db_session` (DBSession): Database session. **(Required)**
        - `otp_type` (OTPType): Type of OTP to request. **(Required)**
        - `background_tasks` (BackgroundTasks): Background tasks for sending
        OTP. **(Required)**
        - `record` (EmailVerifyRequest | ContactNoVerifyRequest |
        PasswordResetRequest): Record containing contact info. **(Required)**
        - `current_user` (CurrentUser): Current user. **(Optional)**

        :Returns:
        - `message` (BaseRead): Success or error message.

        """
        contact_info: PhoneNumber | EmailStr
        user: User | None

        # pylint: disable=no-member
        if otp_type == OTPType.SMS:
            if not isinstance(record, ContactNoVerifyRequest):
                return BaseRead(message=INVALID_REQUEST_TYPE)

            user = self.user_repository.read_by_bulk_fields(
                db_session=db_session,
                fields=[
                    (User.id.key, current_user.id),  # type: ignore
                    (
                        User.contact_no.key,  # type: ignore[union-attr]
                        record.contact_no,
                    ),
                ],
            )

            if not record.contact_no:
                return BaseRead(message=CONTACT_NO_NOT_FOUND)

            contact_info = record.contact_no

        else:
            if not isinstance(
                record, EmailVerifyRequest | PasswordResetRequest
            ):
                return BaseRead(message=INVALID_REQUEST_TYPE)

            user = self.user_repository.read_by_field(
                db_session=db_session,
                field=User.email.key,  # type: ignore[attr-defined]
                value=record.email,
            )

            contact_info = record.email

        if not user:
            return BaseRead(message=USER_NOT_FOUND)

        if not user.is_active:
            return BaseRead(message=INACTIVE_USER)

        # Check for existing OTP record
        otp_record: OTP | None = self.otp_repository.read_by_bulk_fields(
            db_session=db_session,
            fields=[
                (OTP.user_id.key, user.id),  # type: ignore[attr-defined]
                (OTP.otp_type.key, otp_type),  # type: ignore[attr-defined]
            ],
        )

        if (
            otp_record
            and otp_record.is_verified
            and otp_type != OTPType.PASSWORD
        ):
            return BaseRead(message=ALREADY_VERIFIED)

        # Send OTP in background
        background_tasks.add_task(
            func=self.send_otp_background,
            db_session=db_session,
            user=user,
            otp_record=otp_record,
            otp_type=otp_type,
            contact_info=contact_info,
        )

        return BaseRead(message=VERIFICATION_SENT_SUCCESS)

    def _validate_otp_record(
        self,
        db_session: DBSession,
        otp_type: OTPType,
        user_id: int,
        otp_to_verify: str,
    ) -> BaseRead[OTP]:
        """Validate OTP Record.

        :Description:
        - This method validates the OTP record for the given user and OTP type.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `otp_type` (OTPType): Type of OTP being verified. **(Required)**
        - `user_id` (int): Unique identifier for the user. **(Required)**
        - `otp_to_verify` (str): OTP code to verify. **(Required)**

        :Returns:
        - `data` (BaseRead): Data related to OTP validation process.

        """
        # pylint: disable=no-member
        otp_record: OTP | None = self.otp_repository.read_by_bulk_fields(
            db_session=db_session,
            fields=[
                (OTP.user_id.key, user_id),  # type: ignore[attr-defined]
                (OTP.otp_type.key, otp_type),  # type: ignore[attr-defined]
            ],
        )

        if not otp_record or otp_record.otp != otp_to_verify:
            return BaseRead(message=INVALID_OTP)

        if otp_record.is_verified:
            return BaseRead(message=ALREADY_VERIFIED)

        # Check expiry for SMS
        if (
            otp_type == OTPType.SMS
            and otp_record.otp_expiry
            and otp_record.otp_expiry < datetime.now(tz=UTC)
        ):
            return BaseRead(message=EXPIRED_OTP)

        return BaseRead(data=otp_record)

    def verify_otp(
        self,
        db_session: DBSession,
        otp_type: OTPType,
        record: EmailVerify | ContactNoVerify | PasswordReset,
        current_user: CurrentUser | None = None,
    ) -> BaseRead[LoginResponse]:
        """Verify OTP and perform associated action.

        :Description:
        - This method verifies OTP requests for email, SMS, or password reset.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `otp_type` (OTPType): Type of OTP being verified. **(Required)**
        - `record` (EmailVerifyRequest | ContactNoVerifyRequest |
        PasswordResetRequest): Record containing OTP/token info. **(Required)**
        - `current_user` (CurrentUser): Current user. **(Required)**

        :Returns:
        - `data` (BaseRead):Data related to OTP verification process.

        """
        user_id: int
        otp_to_verify: str

        if otp_type == OTPType.SMS and current_user:
            user_id = current_user.id
            otp_to_verify = record.token

        else:
            token_data: dict[str, int | str | datetime | EmailStr] = decode(
                jwt=record.token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            user_id = token_data["id"]  # type: ignore[assignment]
            otp_to_verify = token_data["token"]  # type: ignore[assignment]

        # Validate and get OTP record
        result: BaseRead[OTP] = self._validate_otp_record(
            db_session=db_session,
            otp_type=otp_type,
            user_id=user_id,
            otp_to_verify=otp_to_verify,
        )

        if not result.data:
            return BaseRead(message=result.message)

        otp_record: OTP = result.data

        # Update OTP record
        otp_record.is_verified = True

        if otp_type == OTPType.SMS:
            otp_record.otp_expiry = None

        # pylint: disable=no-member
        self.otp_repository.update_by_id(
            db_session=db_session,
            record_id=otp_record.id,
            record=OTPUpdate(**otp_record.model_dump()),
        )

        if otp_type == OTPType.SMS:
            return BaseRead(message=VERIFICATION_SUCCESS)

        user: User = otp_record.user

        if not user:
            return BaseRead(message=USER_NOT_FOUND)

        if not user.is_active:
            return BaseRead(message=INACTIVE_USER)

        # Handle password reset
        if otp_type == OTPType.PASSWORD:
            if not isinstance(record, PasswordReset):
                return BaseRead(message=INVALID_OTP)

            user.password = UserHelper.get_password_hash(
                password=record.new_password
            )

            self.user_repository.update_by_id(
                db_session=db_session,
                record_id=user.id,
                record=UserUpdate(**user.model_dump()),
            )

        data: dict[str, int | str | EmailStr] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        return BaseRead(
            message=VERIFICATION_SUCCESS,
            data=LoginResponse(
                token_type=TOKEN_TYPE,
                access_token=create_token(
                    data=data, token_type=TokenType.ACCESS_TOKEN
                ),
                refresh_token=create_token(
                    data=data, token_type=TokenType.REFRESH_TOKEN
                ),
                user=user,
            ),
        )
