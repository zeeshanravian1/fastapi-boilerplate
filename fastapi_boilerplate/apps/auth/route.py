"""
Authentication Route Module

Description:
- This module is responsible for handling auth routes.
- It is used to login, refresh token, logout user.

"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from ...database.session import get_session
from .response_message import auth_response_message
from .schema import LoginReadSchema, RefreshToken, RefreshTokenReadSchema
from .view import auth_view

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Login route
@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Perform Authentication",
    response_description="User logged in successfully",
)
async def login(
    db_session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginReadSchema:
    """
    Login.

    Description:
    - This route is used to login user.

    Parameter:
    - **email or username** (STR): Email or username of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**

    Return:
    - **token_type** (STR): Token type of user.
    - **access_token** (STR): Access token of user.
    - **refresh_token** (STR): Refresh token of user.
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Id of role.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: LoginReadSchema | dict[str, str] = await auth_view.login(
        db_session=db_session, form_data=form_data
    )

    if not isinstance(result, LoginReadSchema):
        if result.get("detail") == auth_response_message.USER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=auth_response_message.USER_NOT_FOUND,
            )

        if result.get("detail") == auth_response_message.INCORRECT_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response_message.INCORRECT_PASSWORD,
            )

    return LoginReadSchema.model_validate(obj=result)


# Refresh token route
@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refreshes Authentication Token",
    response_description="Token refreshed successfully",
)
async def refresh_token(
    record: RefreshToken, db_session: Session = Depends(get_session)
) -> RefreshTokenReadSchema:
    """
    Refresh Token.

    Description:
    - This route is used to refresh token.

    Parameter:
    - **record** (STR): Refresh token of user. **(Required)**

    Return:
    - **token_type** (STR): Token type of user.
    - **access_token** (STR): Access token of user.

    """

    result: (
        RefreshTokenReadSchema | dict[str, str]
    ) = await auth_view.refresh_token(db_session=db_session, record=record)

    if not isinstance(result, RefreshTokenReadSchema):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=auth_response_message.USER_NOT_FOUND,
        )

    return RefreshTokenReadSchema.model_validate(obj=result)
