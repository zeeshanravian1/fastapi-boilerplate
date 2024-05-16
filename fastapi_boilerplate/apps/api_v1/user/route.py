"""
User Route Module

Description:
- This module is responsible for handling user routes.
- It is used to create, get, update, delete user details.

"""

from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from fastapi_boilerplate.core.schema import CurrentUserReadSchema
from fastapi_boilerplate.core.security import get_current_active_user
from fastapi_boilerplate.database.session import get_session

from .model import UserTable
from .response_message import user_response_message
from .schema import (
    PasswordChangeReadSchema,
    PasswordChangeSchema,
    UserCreateSchema,
    UserPaginationReadSchema,
    UserPartialUpdateSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from .view import user_view

router = APIRouter(prefix="/user", tags=["User"])


# Create a single user route
@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single user",
    response_description="User created successfully",
)
async def create_user(
    record: UserCreateSchema,
    db_session: Session = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(  # pylint: disable=W0613
        get_current_active_user, scopes=["user:create"]
    ),
) -> UserReadSchema:
    """
    Create a single user

    Description:
    - This route is used to create a single user.

    Parameter:
    User details to be created with following fields:
    - **name** (STR): Name of user. **(Required)**
    - **username** (STR): Username of user. **(Required)**
    - **email** (STR): Email of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**
    - **role_id** (INT): Role ID of user. **(Required)**

    Return:
    User details along with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: UserTable = await user_view.create(
        db_session=db_session, record=record
    )

    return UserReadSchema.model_validate(obj=result)


# Get a single user by id route
@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a single user by providing id",
    response_description="User details fetched successfully",
)
async def get_user_by_id(
    user_id: int,
    db_session: Session = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(  # pylint: disable=W0613
        get_current_active_user, scopes=["user:read"]
    ),
) -> UserReadSchema:
    """
    Get a single user

    Description:
    - This route is used to get a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be fetched. **(Required)**

    Return:
    Get a single user with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: UserTable | None = await user_view.read_by_id(
        db_session=db_session, record_id=user_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Get all users route
@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    response_description="All users fetched successfully",
)
async def get_all_users(
    page: int | None = None,
    limit: int | None = None,
    db_session: Session = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(  # pylint: disable=W0613
        get_current_active_user, scopes=["user:read"]
    ),
) -> UserPaginationReadSchema:
    """
    Get all users

    Description:
    - This route is used to get all users.

    Parameter:
    - **page** (INT): Page number to be fetched. **(Optional)**
    - **limit** (INT): Number of records to be fetched per page. **(Optional)**

    Return:
    Get all users with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: dict[str, int | list] = await user_view.read_all(
        db_session=db_session, page=page, limit=limit
    )

    return UserPaginationReadSchema.model_validate(obj=result)


# Update a single user route
@router.put(
    path="/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single user by providing id",
    response_description="User updated successfully",
)
async def update_user(
    user_id: int,
    record: UserUpdateSchema,
    db_session: Session = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(  # pylint: disable=W0613
        get_current_active_user, scopes=["user:update"]
    ),
) -> UserReadSchema:
    """
    Update a single user

    Description:
    - This route is used to update a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be updated. **(Required)**
    User details to be updated with following fields:
    - **name** (STR): Name of user. **(Required)**
    - **username** (STR): Username of user. **(Required)**
    - **email** (STR): Email of user. **(Required)**
    - **role_id** (INT): Role ID of user. **(Required)**

    Return:
    User details along with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: UserTable | None = await user_view.update(
        db_session=db_session, record_id=user_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Partial update a single user route
@router.patch(
    path="/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partial update a single user by providing id",
    response_description="User updated successfully",
)
async def partial_update_user(
    user_id: int,
    record: UserPartialUpdateSchema,
    db_session: Session = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(  # pylint: disable=W0613
        get_current_active_user, scopes=["user:update"]
    ),
) -> UserReadSchema:
    """
    Partial update a single user

    Description:
    - This route is used to partial update a single user by providing id.

    Parameter:
    - **user_id**: ID of user to be updated. (INT) **(Required)**
    User details to be updated with following fields:
    - **name** (STR): Name of user. **(Optional)**
    - **username** (STR): Username of user. **(Optional)**
    - **email** (STR): Email of user. **(Optional)**
    - **role_id** (INT): Role ID of user. **(Optional)**
    - **password** (STR): Password of user. **(Optional)**

    Return:
    User details along with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: UserTable | None = await user_view.update(
        db_session=db_session,
        record_id=user_id,
        record=record,  # type: ignore
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Delete a single user route
@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single user by providing id",
    response_description="User deleted successfully",
)
async def delete_user(
    user_id: int,
    db_session: Session = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(  # pylint: disable=W0613
        get_current_active_user, scopes=["user:delete"]
    ),
) -> None:
    """
    Delete a single user

    Description:
    - This route is used to delete a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be deleted. **(Required)**

    Return:
    - **None**

    """

    result: UserTable | None = await user_view.delete(
        db_session=db_session, record_id=user_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )


# Change password of a single user route
@router.post(
    path="/change-password",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Change password of a single user",
    response_description="Password changed successfully",
)
async def password_change(
    record: PasswordChangeSchema,
    db_session: Session = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(
        get_current_active_user, scopes=["user:change-password"]
    ),
) -> PasswordChangeReadSchema:
    """
    Change password of a single user

    Description:
    - This route is used to change password of a single user.

    Parameter:
    - **old_password** (STR): Old password of user. **(Required)**
    - **new_password** (STR): New password of user. **(Required)**

    Return:
    - **detail** (STR): Password changed successfully.

    """

    result: dict[str, str] = await user_view.password_change(
        db_session=db_session, record_id=current_user.id, record=record
    )

    if result.get("detail") == user_response_message.USER_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    if result.get("detail") == user_response_message.INCORRECT_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user_response_message.INCORRECT_PASSWORD,
        )

    return PasswordChangeReadSchema.model_validate(obj=result)
