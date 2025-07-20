"""User API Endpoints.

Description:
- This module contains API endpoints for user management.

"""

from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse

from fastapi_boilerplate.apps.base.model import (
    BasePaginationData,
    PaginationQueryParams,
)
from fastapi_boilerplate.apps.base.service_initializer import (
    ServiceInitializer,
)
from fastapi_boilerplate.core.security import CurrentUser
from fastapi_boilerplate.database.session import DBSession

from .constant import USER_NOT_FOUND
from .model import (
    User,
    UserBulkPatch,
    UserBulkRead,
    UserBulkUpdate,
    UserCreate,
    UserPaginationData,
    UserPaginationRead,
    UserPatch,
    UserRead,
    UserResponse,
    UserUpdate,
)
from .service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="User created successfully.",
)
async def create_user(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    record: UserCreate,
) -> UserRead:
    """Create a single user.

    :Description:
    - This route is used to create a single user.

    :Args:
    User details to be created with following fields:
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `contact_no` (str | None): Contact number of user. **(Optional)**
    - `username` (str): Username of user. **(Required)**
    - `email` (str): Email of user. **(Required)**
    - `password` (str): Password of user. **(Required)**
    - `address` (str | None): Address of user. **(Optional)**
    - `city` (str | None): City of user. **(Optional)**
    - `state` (str | None): State of user. **(Optional)**
    - `country` (str | None): Country of user. **(Optional)**
    - `postal_code` (str | None): Postal code of user. **(Optional)**
    - `profile_image_path` (str | None): Path to user's profile image.
    **(Optional)**
    - `is_active` (bool): Status of user account. **(Optional)**

    :Returns:
    User details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """
    user: User = user_service.create(db_session=db_session, record=record)

    return UserRead(
        message="User created successfully",
        data=UserResponse.model_validate(obj=user),
    )


@router.post(
    path="/bulk/",
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple users",
    response_description="Users created successfully",
)
async def create_users(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    records: list[UserCreate],
) -> UserBulkRead:
    """Create multiple users.

    :Description:
    - This route is used to create multiple users.

    :Args:
    List of user details to be created with following fields:
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `contact_no` (str | None): Contact number of user. **(Optional)**
    - `username` (str): Username of user. **(Required)**
    - `email` (str): Email of user. **(Required)**
    - `password` (str): Password of user. **(Required)**
    - `address` (str | None): Address of user. **(Optional)**
    - `city` (str | None): City of user. **(Optional)**
    - `state` (str | None): State of user. **(Optional)**
    - `country` (str | None): Country of user. **(Optional)**
    - `postal_code` (str | None): Postal code of user. **(Optional)**
    - `profile_image_path` (str | None): Path to user's profile image.
    **(Optional)**
    - `is_active` (bool): Status of user account. **(Optional)**

    :Returns:
    List of user details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """
    users: list[User] = user_service.bulk_create(
        db_session=db_session, records=records
    )

    return UserBulkRead(
        message="Users created successfully",
        data=[UserResponse.model_validate(obj=user) for user in users],
    )


@router.get(
    path="/bulk/",
    status_code=status.HTTP_200_OK,
    summary="Retrieve multiple users by IDs",
    response_description="Users retrieved successfully",
)
async def read_users_by_ids(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    user_ids: Annotated[list[UUID | int], Query(...)],
    _: CurrentUser,
) -> UserBulkRead:
    """Retrieve multiple users by their IDs.

    :Description:
    - This route is used to retrieve multiple users by their IDs.

    :Args:
    - `user_ids` (list[UUID | int]): List of user IDs to retrieve.
    **(Required)**

    :Returns:
    List of user details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """
    users: list[User] = user_service.read_bulk_by_ids(
        db_session=db_session, record_ids=user_ids
    )

    return UserBulkRead(
        message="Users retrieved successfully",
        data=[UserResponse.model_validate(obj=user) for user in users],
    )


@router.get(
    path="/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single user by ID",
    response_description="User retrieved successfully",
)
async def read_user_by_id(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    user_id: UUID | int,
    _: CurrentUser,
) -> UserRead:
    """Retrieve a single user by its ID.

    :Description:
    - This route is used to retrieve a single user by its ID.

    :Args:
    - `user_id` (UUID | int): ID of user to retrieve.
    **(Required)**

    :Returns:
    User details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """
    user: User | None = user_service.read_by_id(
        db_session=db_session, record_id=user_id
    )

    if not isinstance(user, User):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": USER_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    return UserRead(
        message="User retrieved successfully",
        data=UserResponse.model_validate(obj=user),
    )


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Retrieve all users",
    response_description="Users retrieved successfully",
)
async def read_all_users(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    params: Annotated[PaginationQueryParams, Depends()],
    _: CurrentUser,
) -> UserPaginationRead:
    """Retrieve all users.

    :Description:
    - This route is used to retrieve all users.

    :Returns:
    List of user details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """
    users: BasePaginationData[User] = user_service.read_all(
        db_session=db_session, params=params
    )

    return UserPaginationRead(
        message="Users retrieved successfully",
        data=UserPaginationData(
            page=users.page,
            limit=users.limit,
            total_pages=users.total_pages,
            total_records=users.total_records,
            records=[
                UserResponse.model_validate(obj=user) for user in users.records
            ],
        ),
    )


@router.put(
    path="/bulk/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update multiple users",
    response_description="Users updated successfully",
)
async def update_users(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    records: Sequence[UserBulkUpdate],
    _: CurrentUser,
) -> UserBulkRead:
    """Update multiple users.

    :Description:
    - This route is used to update multiple users.

    :Args:
    List of user details to be updated with following fields:
    - `id` (UUID | int): ID of user to update. **(Required)**
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `contact_no` (str | None): Contact number of user. **(Optional)**
    - `username` (str): Username of user. **(Required)**
    - `email` (str): Email of user. **(Required)**
    - `address` (str | None): Address of user. **(Optional)**
    - `city` (str | None): City of user. **(Optional)**
    - `state` (str | None): State of user. **(Optional)**
    - `country` (str | None): Country of user. **(Optional)**
    - `postal_code` (str | None): Postal code of user. **(Optional)**
    - `profile_image_path` (str | None): Path to user's profile image.
    **(Optional)**
    - `is_active` (bool): Status of user account. **(Optional)**

    :Returns:
    List of updated user details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """
    updated_users: list[User] = user_service.update_bulk_by_ids(
        db_session=db_session, records=records
    )

    return UserBulkRead(
        message="Users updated successfully",
        data=[UserResponse.model_validate(obj=user) for user in updated_users],
    )


@router.put(
    path="/{user_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a user",
    response_description="User updated successfully",
)
async def update_user(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    user_id: UUID | int,
    record: UserUpdate,
    _: CurrentUser,
) -> UserRead:
    """Update a single user.

    :Description:
    - This route is used to update a single user.

    :Args:
    - `user_id` (UUID | int): ID of user to update. **(Required)**

    User details to be updated with following fields:
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `contact_no` (str | None): Contact number of user. **(Optional)**
    - `username` (str): Username of user. **(Required)**
    - `email` (str): Email of user. **(Required)**
    - `address` (str | None): Address of user. **(Optional)**
    - `city` (str | None): City of user. **(Optional)**
    - `state` (str | None): State of user. **(Optional)**
    - `country` (str | None): Country of user. **(Optional)**
    - `postal_code` (str | None): Postal code of user. **(Optional)**
    - `profile_image_path` (str | None): Path to user's profile image.
    **(Optional)**
    - `is_active` (bool): Status of user account. **(Optional)**

    :Returns:
    User details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.

    """
    updated_user: User | None = user_service.update_by_id(
        db_session=db_session, record_id=user_id, record=record
    )

    if not isinstance(updated_user, User):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": USER_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    return UserRead(
        message="User updated successfully",
        data=UserResponse.model_validate(obj=updated_user),
    )


@router.patch(
    path="/bulk/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partially update multiple users",
    response_description="Users partially updated successfully",
)
async def patch_users(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    records: Sequence[UserBulkPatch],
    _: CurrentUser,
) -> UserBulkRead:
    """Partially update multiple users.

    :Description:
    - This route is used to partially update multiple users.

    :Args:
    List of user details to be partially updated with following fields:
    - `id` (UUID | int): ID of user to update. **(Required)**
    - `first_name` (str): First name of user. **(Optional)**
    - `last_name` (str): Last name of user. **(Optional)**
    - `contact_no` (str | None): Contact number of user. **(Optional)**
    - `username` (str): Username of user. **(Optional)**
    - `email` (str): Email of user. **(Optional)**
    - `address` (str | None): Address of user. **(Optional)**
    - `city` (str | None): City of user. **(Optional)**
    - `state` (str | None): State of user. **(Optional)**
    - `country` (str | None): Country of user. **(Optional)**
    - `postal_code` (str | None): Postal code of user. **(Optional)**
    - `profile_image_path` (str | None): Path to user's profile image.
    **(Optional)**
    - `is_active` (bool): Status of user account. **(Optional)**

    :Returns:
    List of updated user details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    updated_users: list[User] = user_service.update_bulk_by_ids(
        db_session=db_session, records=records
    )

    return UserBulkRead(
        message="Users partially updated successfully",
        data=[UserResponse.model_validate(obj=user) for user in updated_users],
    )


@router.patch(
    path="/{user_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partially update a user",
    response_description="User partially updated successfully",
)
async def patch_user(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    user_id: UUID | int,
    record: UserPatch,
    _: CurrentUser,
) -> UserRead:
    """Partially update a single user.

    :Description:
    - This route is used to partially update a single user.

    :Args:
    - `user_id` (UUID | int): ID of user to update. **(Required)**

    User details to be partially updated with following fields:
    - `first_name` (str): First name of user. **(Optional)**
    - `last_name` (str): Last name of user. **(Optional)**
    - `contact_no` (str | None): Contact number of user. **(Optional)**
    - `username` (str): Username of user. **(Optional)**
    - `email` (str): Email of user. **(Optional)**
    - `address` (str | None): Address of user. **(Optional)**
    - `city` (str | None): City of user. **(Optional)**
    - `state` (str | None): State of user. **(Optional)**
    - `country` (str | None): Country of user. **(Optional)**
    - `postal_code` (str | None): Postal code of user. **(Optional)**
    - `profile_image_path` (str | None): Path to user's profile image.
    **(Optional)**
    - `is_active` (bool): Status of user account. **(Optional)**

    :Returns:
    User details along with following fields:
    - `id` (UUID | int): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `contact_no` (str | None): Contact number of user.
    - `username` (str): Username of user.
    - `email` (str): Email of user.
    - `address` (str | None): Address of user.
    - `city` (str | None): City of user.
    - `state` (str | None): State of user.
    - `country` (str | None): Country of user.
    - `postal_code` (str | None): Postal code of user.
    - `profile_image_path` (str | None): Path to user's profile image.
    - `is_active` (bool): Status of user account.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    updated_user: User | None = user_service.update_by_id(
        db_session=db_session,
        record_id=user_id,
        record=record,  # type: ignore[arg-type]
    )

    if not isinstance(updated_user, User):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": USER_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    return UserRead(
        message="User partially updated successfully",
        data=UserResponse.model_validate(obj=updated_user),
    )


@router.delete(
    path="/bulk/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete multiple users",
    response_description="Users deleted successfully",
)
async def delete_users(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    user_ids: Annotated[list[UUID | int], Query(...)],
    _: CurrentUser,
) -> None:
    """Delete multiple users.

    :Description:
    - This route is used to delete multiple users by their IDs.

    :Args:
    - `user_ids` (list[UUID | int]): List of user IDs to delete. **(Required)**

    :Returns:
    - `None`

    """
    user_service.delete_bulk_by_ids(db_session=db_session, record_ids=user_ids)


@router.delete(
    path="/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    response_description="User deleted successfully",
)
async def delete_user(
    db_session: DBSession,
    user_service: Annotated[
        UserService, Depends(dependency=ServiceInitializer(UserService))
    ],
    user_id: UUID | int,
    _: CurrentUser,
) -> None:
    """Delete a single user.

    :Description:
    - This route is used to delete a single user by its ID.

    :Args:
    - `user_id` (UUID | int): ID of user to delete. **(Required)**

    :Returns:
    - `None`

    """
    result: bool = user_service.delete_by_id(
        db_session=db_session, record_id=user_id
    )

    if not result:
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": USER_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )
