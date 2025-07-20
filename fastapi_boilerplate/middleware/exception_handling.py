"""Exception Middleware.

Description:
- This module contains all exception handling middleware.

"""

import logging
from typing import Any

from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse
from jwt import ExpiredSignatureError, InvalidSignatureError
from psycopg.errors import (
    ForeignKeyViolation,
    NotNullViolation,
    UniqueViolation,
)
from sqlalchemy.exc import IntegrityError

from .constant import (
    FOREIGN_KEY_VIOLATION,
    INTEGRITY_ERROR,
    INTERNAL_SERVER_ERROR,
    INVALID_TOKEN,
    NOT_NULL_VIOLATION,
    TOKEN_EXPIRED,
    UNIQUE_VIOLATION,
)

exception_logger: logging.Logger = logging.getLogger(__name__)


async def exception_handling(
    request: Request, call_next: Any
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
    try:
        response: Response = await call_next(request)

    except ExpiredSignatureError:
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": TOKEN_EXPIRED,
                "data": None,
                "error": TOKEN_EXPIRED,
            },
        )

    except InvalidSignatureError:
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": INVALID_TOKEN,
                "data": None,
                "error": INVALID_TOKEN,
            },
        )

    except IntegrityError as err:
        err_message: str = INTEGRITY_ERROR

        if isinstance(
            err.orig, UniqueViolation | ForeignKeyViolation | NotNullViolation
        ):
            err_message_detail: str | None = err.orig.diag.message_detail

            print(err_message_detail)

            if err_message_detail is not None:
                err_message = (
                    err_message_detail.replace("Key", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace('"', "'")
                    .rstrip(".")
                    .strip()
                )

            elif isinstance(err.orig, UniqueViolation):
                err_message = UNIQUE_VIOLATION

            elif isinstance(err.orig, ForeignKeyViolation):
                err_message = FOREIGN_KEY_VIOLATION

            elif isinstance(err.orig, NotNullViolation):
                err_message = NOT_NULL_VIOLATION

        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": INTEGRITY_ERROR,
                "data": None,
                "error": err_message,
            },
        )

    except Exception as err:  # pylint: disable=broad-exception-caught
        exception_logger.exception(msg=err)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": INTERNAL_SERVER_ERROR,
                "data": None,
                "error": str(err),
            },
        )

    return response
