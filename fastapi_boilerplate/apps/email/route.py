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
from fastapi_boilerplate.database.session import DBSession

from .constant import (
    EMAIL_ALREADY_VERIFIED,
    EMAIL_SENT_SUCCESS,
    EMAIL_VERIFY_PURPOSE,
)
from .model import (
    EmailVerify,
    EmailVerifyRead,
    EmailVerifyRequest,
    EmailVerifyRequestRead,
)
from .service import OTPService

router = APIRouter(prefix="/email", tags=["Email"])


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
