"""OTP Route Module.

Description:
- This module is responsible for handling otp routes.
- It is used to verify email address, verify phone number, and reset password.

"""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import ORJSONResponse

from fastapi_boilerplate.apps.api_v1.user.constant import USER_NOT_FOUND
from fastapi_boilerplate.apps.auth.model import LoginResponse
from fastapi_boilerplate.apps.base.model import BaseRead
from fastapi_boilerplate.apps.base.service_initializer import (
    ServiceInitializer,
)
from fastapi_boilerplate.core.security import CurrentUser
from fastapi_boilerplate.database.session import DBSession

from .constant import (
    EXPIRED_OTP,
    INVALID_OTP,
    PASSWORD_RESET_SUCCESS,
    VERIFICATION_SENT_SUCCESS,
    VERIFICATION_SUCCESS,
    OTPType,
)
from .model import (
    OTP,
    ContactNoVerify,
    ContactNoVerifyRequest,
    EmailVerify,
    EmailVerifyRequest,
    PasswordReset,
    PasswordResetRequest,
)
from .service import OTPService

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.post(
    path="/verify-email-request/",
    status_code=status.HTTP_200_OK,
    summary="Request Verify Email",
    response_description=VERIFICATION_SENT_SUCCESS,
)
async def verify_email_request(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: EmailVerifyRequest,
    background_tasks: BackgroundTasks,
) -> BaseRead[OTP]:
    """Email Verify Request.

    :Description:
    - This route is used to request email verification.

    :Args:
    - `email` (str): Email of user to be verified. **(Required)**

    :Returns:
    - `message` (str): Email sent successfully.

    """
    result: BaseRead[OTP] = await otp_service.request_otp(
        db_session=db_session,
        otp_type=OTPType.EMAIL,
        background_tasks=background_tasks,
        record=record,
    )

    if result.message == USER_NOT_FOUND:
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": USER_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    if result.message != VERIFICATION_SENT_SUCCESS:
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": result.message,
                "data": None,
                "error": None,
            },
        )

    return BaseRead(message=VERIFICATION_SENT_SUCCESS)


@router.post(
    path="/verify-email/",
    status_code=status.HTTP_200_OK,
    summary="Email verification.",
    response_description=VERIFICATION_SUCCESS,
)
async def verify_email(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: EmailVerify,
) -> BaseRead[LoginResponse]:
    """Email Verify.

    :Description:
    - This route is used to verify email.

    :Args:
    - `email` (str): Email of user to be verified. **(Required)**
    - `otp` (str): OTP to verify email. **(Required)**

    :Returns:
    - `message` (str): Email verified successfully.

    """
    result: BaseRead[LoginResponse] = otp_service.verify_otp(
        db_session=db_session, otp_type=OTPType.EMAIL, record=record
    )

    if result.message == USER_NOT_FOUND:
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": USER_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    if result.message in (INVALID_OTP, EXPIRED_OTP):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": result.message,
                "data": None,
                "error": None,
            },
        )

    if result.message != VERIFICATION_SUCCESS:
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": result.message,
                "data": None,
                "error": None,
            },
        )

    return BaseRead(message=VERIFICATION_SUCCESS)


@router.post(
    path="/verify-contact-no-request/",
    status_code=status.HTTP_200_OK,
    summary="Request Verify Contact Number",
    response_description=VERIFICATION_SENT_SUCCESS,
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
) -> BaseRead[OTP]:
    """Contact Number Verify Request.

    :Description:
    - This route is used to request contact number verification.

    :Args:
    - `contact_no` (PhoneNumber): Contact number of user to be verified.
    **(Required)**

    :Returns:
    - `message` (str): Contact number sent successfully.

    """
    return await otp_service.request_otp(
        db_session=db_session,
        otp_type=OTPType.SMS,
        background_tasks=background_tasks,
        record=record,
        current_user=current_user,
    )


@router.post(
    path="/verify-contact-no/",
    status_code=status.HTTP_200_OK,
    summary="Contact Number Verification",
    response_description=VERIFICATION_SUCCESS,
)
async def verify_contact_no(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: ContactNoVerify,
    current_user: CurrentUser,
) -> BaseRead[LoginResponse]:
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
    return otp_service.verify_otp(
        db_session=db_session,
        otp_type=OTPType.SMS,
        record=record,
        current_user=current_user,
    )


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
) -> BaseRead[OTP]:
    """Password Reset Request.

    :Description:
    - This route is used to request password reset.

    :Args:
    - `email` (str): Email of user to reset password. **(Required)**

    :Returns:
    - `message` (str): Password reset email sent successfully.

    """
    return await otp_service.request_otp(
        db_session=db_session,
        otp_type=OTPType.PASSWORD,
        background_tasks=background_tasks,
        record=record,
    )


@router.post(
    path="/reset-password/",
    status_code=status.HTTP_200_OK,
    summary="Reset Password",
    response_description=PASSWORD_RESET_SUCCESS,
)
async def reset_password(
    db_session: DBSession,
    otp_service: Annotated[
        OTPService,
        Depends(dependency=ServiceInitializer(service_class=OTPService)),
    ],
    record: PasswordReset,
) -> BaseRead[LoginResponse]:
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
    return otp_service.verify_otp(
        db_session=db_session, otp_type=OTPType.PASSWORD, record=record
    )
