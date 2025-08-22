"""Exception Middleware.

Description:
- This module contains all exception handling middleware.

"""

import logging
from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse
from jwt import ExpiredSignatureError, InvalidSignatureError
from psycopg.errors import (
    ForeignKeyViolation,
    NotNullViolation,
    UniqueViolation,
)
from sqlalchemy.exc import IntegrityError

from fastapi_boilerplate.apps.otp.constant import EXPIRED_OTP, INVALID_OTP

from .constant import INTEGRITY_ERROR, INTERNAL_SERVER_ERROR

exception_logger: logging.Logger = logging.getLogger(__name__)


class ExceptionHandlingMiddleware:  # pylint: disable=too-few-public-methods
    """Exception Handling Middleware.

    :Description:
    - This class is used to handle exceptions.

    """

    @staticmethod
    async def exception_handling(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> ORJSONResponse | Response:
        """Exception Handling Middleware.

        :Description:
        - This function is used to handle exceptions.

        :Args:
        - `request` (Request): Request object. **(Required)**
        - `call_next` (Callable): Next function to be called. **(Required)**

        :Returns:
        - **response** (Response): Response object.

        """
        message: str
        error: str | None = None

        try:
            response: Response = await call_next(request)
            return response

        except ExpiredSignatureError:
            status_code = status.HTTP_401_UNAUTHORIZED
            message = EXPIRED_OTP

        except InvalidSignatureError:
            status_code = status.HTTP_401_UNAUTHORIZED
            message = INVALID_OTP

        except IntegrityError as err:
            status_code = status.HTTP_409_CONFLICT
            message = INTEGRITY_ERROR
            error = INTEGRITY_ERROR

            if isinstance(
                err.orig,
                UniqueViolation | ForeignKeyViolation | NotNullViolation,
            ):
                err_message_detail: str | None = err.orig.diag.message_detail

                if err_message_detail is not None:
                    error = (
                        err_message_detail.replace("Key", "")
                        .replace("(", "")
                        .replace(")", "")
                        .replace('"', "'")
                        .rstrip(".")
                        .strip()
                    )

        except Exception as err:  # pylint: disable=broad-exception-caught
            exception_logger.exception(msg=err)

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = INTERNAL_SERVER_ERROR
            error = str(err)

        return ORJSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "data": None,
                "error": error,
            },
        )
