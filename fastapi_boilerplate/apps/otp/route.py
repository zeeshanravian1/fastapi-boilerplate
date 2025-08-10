"""OTP Route Module.

Description:
- This module is responsible for handling otp routes.
- It is used to verify email address, verify phone number, and reset password.

"""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import ORJSONResponse

from fastapi_boilerplate.apps.api_v1.user.constant import (
    INACTIVE_USER,
    USER_NOT_FOUND,
)
from fastapi_boilerplate.apps.base.service_initializer import (
    ServiceInitializer,
)
from fastapi_boilerplate.core.security import CurrentUser
from fastapi_boilerplate.database.session import DBSession

from .constant import (
    CONTACT_NO_SENT_SUCCESS,
    CONTACT_NO_VERIFIED,
    CONTACT_NO_VERIFIED_SUCCESS,
    CONTACT_NO_VERIFY_PURPOSE,
    EMAIL_ALREADY_VERIFIED,
    EMAIL_SENT_SUCCESS,
    EMAIL_VERIFY_PURPOSE,
    EXPIRED_OTP,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_RESET_PURPOSE,
)
from .model import (
    ContactNoVerify,
    ContactNoVerifyRead,
    ContactNoVerifyRequest,
    ContactNoVerifyRequestRead,
    EmailVerify,
    EmailVerifyRead,
    EmailVerifyRequest,
    EmailVerifyRequestRead,
    PasswordReset,
    PasswordResetRead,
    PasswordResetRequest,
    PasswordResetRequestRead,
)
from .service import OTPService

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.post(
    path="/verify-email-request/",
    status_code=status.HTTP_200_OK,
    summary="Request Verify Email",
    response_description=EMAIL_SENT_SUCCESS,
)
async def verify_email_request(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: EmailVerifyRequest,
    background_tasks: BackgroundTasks,
) -> EmailVerifyRequestRead:
    """Email Verify Request.

    :Description:
    - This route is used to request email verification.

    :Args:
    - `email` (str): Email of user to be verified. **(Required)**

    :Returns:
    - `message` (str): Email sent successfully.

    """
    result: str | None = await otp_service.verify_email_request(
        db_session=db_session, record=record, background_tasks=background_tasks
    )

    if isinstance(result, str):
        if result == USER_NOT_FOUND:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": USER_NOT_FOUND,
                    "data": None,
                    "error": None,
                },
            )

        if result == INACTIVE_USER:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "success": False,
                    "message": INACTIVE_USER,
                    "data": None,
                    "error": None,
                },
            )

        if result == EMAIL_ALREADY_VERIFIED:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": EMAIL_ALREADY_VERIFIED,
                    "data": None,
                    "error": None,
                },
            )

    return EmailVerifyRequestRead(message=EMAIL_SENT_SUCCESS)


@router.post(
    path="/verify-email/",
    status_code=status.HTTP_200_OK,
    summary=EMAIL_VERIFY_PURPOSE,
    response_description="Email verified successfully.",
)
async def verify_email(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: EmailVerify,
) -> EmailVerifyRead:
    """Email Verify.

    :Description:
    - This route is used to verify email.

    :Args:
    - `email` (str): Email of user to be verified. **(Required)**
    - `otp` (str): OTP to verify email. **(Required)**

    :Returns:
    - `message` (str): Email verified successfully.

    """
    return otp_service.verify_email(db_session=db_session, record=record)


@router.post(
    path="/verify-contact-no-request/",
    status_code=status.HTTP_200_OK,
    summary="Request Verify Contact Number",
    response_description=CONTACT_NO_SENT_SUCCESS,
)
async def verify_contact_no_request(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: ContactNoVerifyRequest,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
) -> ContactNoVerifyRequestRead:
    """Contact Number Verify Request.

    :Description:
    - This route is used to request contact number verification.

    :Args:
    - `contact_no` (PhoneNumber): Contact number of user to be verified.
    **(Required)**

    :Returns:
    - `message` (str): Contact number sent successfully.

    """
    result: str | None = await otp_service.verify_contact_no_request(
        db_session=db_session,
        record=record,
        current_user=current_user,
        background_tasks=background_tasks,
    )

    if isinstance(result, str):
        if result == USER_NOT_FOUND:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": USER_NOT_FOUND,
                    "data": None,
                    "error": None,
                },
            )

        if result == INACTIVE_USER:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "success": False,
                    "message": INACTIVE_USER,
                    "data": None,
                    "error": None,
                },
            )

        if result == CONTACT_NO_VERIFIED:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": CONTACT_NO_VERIFIED,
                    "data": None,
                    "error": None,
                },
            )

    return ContactNoVerifyRequestRead(message=CONTACT_NO_SENT_SUCCESS)


@router.post(
    path="/verify-contact-no/",
    status_code=status.HTTP_200_OK,
    summary=CONTACT_NO_VERIFY_PURPOSE,
    response_description=CONTACT_NO_VERIFIED_SUCCESS,
)
async def verify_contact_no(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: ContactNoVerify,
    current_user: CurrentUser,
) -> ContactNoVerifyRead:
    """Contact Number Verify.

    :Description:
    - This route is used to verify contact number.

    :Args:
    - `contact_no` (PhoneNumber): Contact number of user to be verified.
    **(Required)**
    - `otp` (str): OTP to verify contact number. **(Required)**

    :Returns:
    - `message` (str): Contact number verified successfully.

    """
    result: ContactNoVerifyRead = otp_service.verify_contact_no(
        db_session=db_session, record=record, current_user=current_user
    )

    if isinstance(result, str):
        if result == EXPIRED_OTP:
            return ORJSONResponse(  # type: ignore[return-value, unused-ignore]
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": EXPIRED_OTP,
                    "data": None,
                    "error": None,
                },
            )

        return ORJSONResponse(  # type: ignore[return-value, unused-ignore]
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": result,
                "data": None,
                "error": None,
            },
        )

    return result


@router.post(
    path="/reset-password-request/",
    status_code=status.HTTP_200_OK,
    summary="Request Reset Password",
    response_description="Password reset email sent successfully.",
)
async def reset_password_request(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: PasswordResetRequest,
    background_tasks: BackgroundTasks,
) -> PasswordResetRequestRead:
    """Password Reset Request.

    :Description:
    - This route is used to request password reset.

    :Args:
    - `email` (str): Email of user to reset password. **(Required)**

    :Returns:
    - `message` (str): Password reset email sent successfully.

    """
    result: str | None = await otp_service.reset_password_request(
        db_session=db_session, record=record, background_tasks=background_tasks
    )

    if isinstance(result, str):
        if result == USER_NOT_FOUND:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": USER_NOT_FOUND,
                    "data": None,
                    "error": None,
                },
            )

        if result == INACTIVE_USER:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "success": False,
                    "message": INACTIVE_USER,
                    "data": None,
                    "error": None,
                },
            )

    return PasswordResetRequestRead(message=EMAIL_SENT_SUCCESS)


@router.post(
    path="/reset-password/",
    status_code=status.HTTP_200_OK,
    summary=PASSWORD_RESET_PURPOSE,
    response_description=PASSWORD_CHANGE_SUCCESS,
)
async def reset_password(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: PasswordReset,
) -> PasswordResetRead:
    """Password Reset.

    :Description:
    - This route is used to reset password.

    :Args:
    - `email` (str): Email of user to reset password. **(Required)**
    - `otp` (str): OTP to reset password. **(Required)**
    - `new_password` (str): New password to set. **(Required)**

    :Returns:
    - `message` (str): Password changed successfully.

    """
    return otp_service.reset_password(db_session=db_session, record=record)
