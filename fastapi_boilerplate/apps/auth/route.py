"""Authentication Route Module.

Description:
- This module is responsible for handling auth routes.
- It is used to login, refresh token.

"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_boilerplate.apps.api_v1.user.constant import (
    INACTIVE_USER,
    USER_NOT_FOUND,
)
from fastapi_boilerplate.apps.base.service_initializer import (
    ServiceInitializer,
)
from fastapi_boilerplate.database.session import DBSession

from .constant import INCORRECT_PASSWORD
from .model import (
    LoginResponse,
    RefreshToken,
    RefreshTokenRead,
    RefreshTokenResponse,
)
from .service import AuthenticationService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    path="/login/",
    status_code=status.HTTP_200_OK,
    summary="Perform Authentication",
    response_description="User logged in successfully",
)
async def login(
    db_session: DBSession,
    auth_service: Annotated[
        AuthenticationService,
        Depends(
            dependency=ServiceInitializer(service_class=AuthenticationService)
        ),
    ],
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginResponse:
    """Login.

    :Description:
    - This route is used to login user.

    :Args:
    - `username` (str): Email or username of user. **(Required)**
    - `password` (str): Password of user. **(Required)**

    :Returns:
    - `token_type` (str): Type of token.
    - `access_token` (str): Access token.
    - `refresh_token` (str): Refresh token.

    """
    result: LoginResponse | str = auth_service.login(
        db_session=db_session,
        form_data=form_data,
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

        if result == INCORRECT_PASSWORD:
            return ORJSONResponse(  # type: ignore[return-value]
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message": INCORRECT_PASSWORD,
                    "data": None,
                    "error": None,
                },
            )

    return LoginResponse(**result.model_dump())  # type: ignore[union-attr]


@router.post(
    path="/refresh-token/",
    status_code=status.HTTP_200_OK,
    summary="Refresh Token",
    response_description="Token refreshed successfully",
)
async def refresh_token(
    db_session: DBSession,
    token: RefreshToken,
    auth_service: Annotated[
        AuthenticationService,
        Depends(
            dependency=ServiceInitializer(service_class=AuthenticationService)
        ),
    ],
) -> RefreshTokenRead:
    """Refresh Token.

    :Description:
    - This route is used to refresh token.

    :Args:
    - `token` (str): Token to refresh. **(Required)**
    - `db_session` (DBSession): Database session. **(Required)**

    :Returns:
    - **token_type** (str): Token type of user.
    - **access_token** (str): Access token of user.

    """
    result: RefreshTokenResponse | str = auth_service.refresh_token(
        db_session=db_session,
        token=token.refresh_token,
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

    return RefreshTokenRead(
        success=True,
        message="Token refreshed successfully",
        data=RefreshTokenResponse(**result.model_dump()),  # type: ignore
    )
