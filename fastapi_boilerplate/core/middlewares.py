"""
Middlewares Module

Description:
- This module contains all middlewares used in project.

"""

import logging
import re
from typing import Any

from fastapi import Request, Response, status
from fastapi.exceptions import HTTPException, ResponseValidationError
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.exc import IntegrityError

from .response_message import core_response_message

exception_logger: logging.Logger = logging.getLogger(__name__)
exception_logger.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

exception_logger.addHandler(console_handler)


async def exception_handling(
    request: Request, call_next
) -> JSONResponse | Any | Response:
    """
    Exception Handling Middleware

    Description:
    - This function is used to handle exceptions.

    Parameter:
    - **request** (Request): Request object. **(Required)**
    - **call_next** (Callable): Next function to be called. **(Required)**

    Return:
    - **response** (Response): Response object.

    """

    try:
        response: Response = await call_next(request)

    except ExpiredSignatureError:
        content: dict[str, str] = {
            "detail": core_response_message.TOKEN_EXPIRED
        }
        status_code = status.HTTP_401_UNAUTHORIZED

    except JWTError:
        content = {"detail": core_response_message.INVALID_TOKEN}
        status_code = status.HTTP_401_UNAUTHORIZED

    except IntegrityError as err:
        err_message: str = str(err.orig.args[1])  # type: ignore

        if err_message.startswith("Duplicate entry"):
            values: list[str] = re.findall(r"'(.*?)'", err_message)
            detail: str = (
                f"{values[0]}={values[1].split(".")[-1]} already exists"
            )

        elif err_message.endswith("cannot be null"):
            detail = err_message.replace("Column", "").strip()

        elif "foreign key constraint fails" in err_message:
            match: re.Match[str] | None = re.search(
                r"FOREIGN KEY \(`(.*?)`\)", err_message
            )
            detail = (
                f"'{match.group(1)}' does not exist"
                if match
                else "Foreign key constraint failed"
            )

        else:
            exception_logger.exception(msg=err)
            detail = core_response_message.INTEGRITY_ERROR

        content = {"detail": detail}
        status_code = status.HTTP_409_CONFLICT

    except ResponseValidationError as err:
        exception_logger.exception(msg=err)
        content = {"detail": core_response_message.INVALID_RESPONSE_BODY}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    except HTTPException as err:
        exception_logger.exception(msg=err)
        content = {"message": err.detail}
        status_code = err.status_code

    except Exception as err:  # pylint: disable=W0718
        exception_logger.exception(msg=err)
        content = {"detail": core_response_message.INTERNAL_SERVER_ERROR}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        return response

    return JSONResponse(status_code=status_code, content=content)
