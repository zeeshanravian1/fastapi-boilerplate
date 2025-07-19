"""Role API Endpoints.

Description:
- This module contains API endpoints for role management.

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
from fastapi_boilerplate.database.session import DBSession

from .constant import ROLE_NOT_FOUND
from .model import (
    Role,
    RoleBulkPatch,
    RoleBulkRead,
    RoleBulkUpdate,
    RoleCreate,
    RolePaginationData,
    RolePaginationRead,
    RolePatch,
    RoleRead,
    RoleResponse,
    RoleUpdate,
)
from .service import RoleService

router = APIRouter(prefix="/role", tags=["Role"])


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new role",
    response_description="Role created successfully.",
)
async def create_role(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    record: RoleCreate,
) -> RoleRead:
    """Create a single role.

    :Description:
    - This route is used to create a single role.

    :Args:
    Role details to be created with following fields:
    - `role_name` (str): Name of role. **(Required)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    Role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    role: Role = role_service.create(db_session=db_session, record=record)

    return RoleRead(
        message="Role created successfully",
        data=RoleResponse.model_validate(obj=role),
    )


@router.post(
    path="/bulk/",
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple roles",
    response_description="Roles created successfully",
)
async def create_roles(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    records: list[RoleCreate],
) -> RoleBulkRead:
    """Create multiple roles.

    :Description:
    - This route is used to create multiple roles.

    :Args:
    List of role details to be created with following fields:
    - `role_name` (str): Name of role. **(Required)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    List of role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    roles: list[Role] = role_service.bulk_create(
        db_session=db_session, records=records
    )

    return RoleBulkRead(
        message="Roles created successfully",
        data=[RoleResponse.model_validate(obj=role) for role in roles],
    )


@router.get(
    path="/bulk/",
    status_code=status.HTTP_200_OK,
    summary="Retrieve multiple roles by IDs",
    response_description="Roles retrieved successfully",
)
async def read_roles_by_ids(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    role_ids: Annotated[list[UUID | int], Query(...)],
) -> RoleBulkRead:
    """Retrieve multiple roles by their IDs.

    :Description:
    - This route is used to retrieve multiple roles by their IDs.

    :Args:
    - `role_ids` (list[UUID | int]): List of role IDs to retrieve.
    **(Required)**

    :Returns:
    List of role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    roles: list[Role] = role_service.read_bulk_by_ids(
        db_session=db_session, record_ids=role_ids
    )

    return RoleBulkRead(
        message="Roles retrieved successfully",
        data=[RoleResponse.model_validate(obj=role) for role in roles],
    )


@router.get(
    path="/{role_id}/",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single role by ID",
    response_description="Role retrieved successfully",
)
async def read_role_by_id(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    role_id: UUID | int,
) -> RoleRead:
    """Retrieve a single role by its ID.

    :Description:
    - This route is used to retrieve a single role by its ID.

    :Args:
    - `role_id` (UUID | int): ID of role to retrieve.
    **(Required)**

    :Returns:
    Role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    role: Role | None = role_service.read_by_id(
        db_session=db_session, record_id=role_id
    )

    if not isinstance(role, Role):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": ROLE_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    return RoleRead(
        message="Role retrieved successfully",
        data=RoleResponse.model_validate(obj=role),
    )


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Retrieve all roles",
    response_description="Roles retrieved successfully",
)
async def read_all_roles(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    params: Annotated[PaginationQueryParams, Depends()],
) -> RolePaginationRead:
    """Retrieve all roles.

    :Description:
    - This route is used to retrieve all roles.

    :Returns:
    List of role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    roles: BasePaginationData[Role] = role_service.read_all(
        db_session=db_session, params=params
    )

    return RolePaginationRead(
        message="Roles retrieved successfully",
        data=RolePaginationData(
            page=roles.page,
            limit=roles.limit,
            total_pages=roles.total_pages,
            total_records=roles.total_records,
            records=[
                RoleResponse.model_validate(obj=role) for role in roles.records
            ],
        ),
    )


@router.put(
    path="/bulk/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update multiple roles",
    response_description="Roles updated successfully",
)
async def update_roles(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    records: Sequence[RoleBulkUpdate],
) -> RoleBulkRead:
    """Update multiple roles.

    :Description:
    - This route is used to update multiple roles.

    :Args:
    List of role details to be updated with following fields:
    - `role_name` (str): Name of role. **(Required)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    List of updated role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    updated_roles: list[Role] = role_service.update_bulk_by_ids(
        db_session=db_session, records=records
    )

    return RoleBulkRead(
        message="Roles updated successfully",
        data=[RoleResponse.model_validate(obj=role) for role in updated_roles],
    )


@router.put(
    path="/{role_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a role",
    response_description="Role updated successfully",
)
async def update_role(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    role_id: UUID | int,
    record: RoleUpdate,
) -> RoleRead:
    """Update a single role.

    :Description:
    - This route is used to update a single role.

    :Args:
    - `role_id` (UUID | int): ID of role to update. **(Required)**

    Role details to be updated with following fields:
    - `role_name` (str): Name of role. **(Required)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    Role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    updated_role: Role | None = role_service.update_by_id(
        db_session=db_session, record_id=role_id, record=record
    )

    if not isinstance(updated_role, Role):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": ROLE_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    return RoleRead(
        message="Role updated successfully",
        data=RoleResponse.model_validate(obj=updated_role),
    )


@router.patch(
    path="/bulk/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partially update multiple roles",
    response_description="Roles partially updated successfully",
)
async def patch_roles(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    records: Sequence[RoleBulkPatch],
) -> RoleBulkRead:
    """Partially update multiple roles.

    :Description:
    - This route is used to partially update multiple roles.

    :Args:
    List of role details to be partially updated with following fields:
    - `role_name` (str): Name of role. **(Optional)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    List of updated role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    updated_roles: list[Role] = role_service.update_bulk_by_ids(
        db_session=db_session, records=records
    )

    return RoleBulkRead(
        message="Roles partially updated successfully",
        data=[RoleResponse.model_validate(obj=role) for role in updated_roles],
    )


@router.patch(
    path="/{role_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partially update a role",
    response_description="Role partially updated successfully",
)
async def patch_role(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    role_id: UUID | int,
    record: RolePatch,
) -> RoleRead:
    """Partially update a single role.

    :Description:
    - This route is used to partially update a single role.

    :Args:
    - `role_id` (UUID | int): ID of role to update. **(Required)**

    Role details to be partially updated with following fields:
    - `role_name` (str): Name of role. **(Optional)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    Role details along with following fields:
    - `id` (UUID | int): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    updated_role: Role | None = role_service.update_by_id(
        db_session=db_session,
        record_id=role_id,
        record=record,  # type: ignore[arg-type]
    )

    if not isinstance(updated_role, Role):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": ROLE_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )

    return RoleRead(
        message="Role partially updated successfully",
        data=RoleResponse.model_validate(obj=updated_role),
    )


@router.delete(
    path="/bulk/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete multiple roles",
    response_description="Roles deleted successfully",
)
async def delete_roles(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    role_ids: Annotated[list[UUID | int], Query(...)],
) -> None:
    """Delete multiple roles.

    :Description:
    - This route is used to delete multiple roles by their IDs.

    :Args:
    - `role_ids` (list[UUID | int]): List of role IDs to delete. **(Required)**

    :Returns:
    - `None`

    """
    role_service.delete_bulk_by_ids(db_session=db_session, record_ids=role_ids)


@router.delete(
    path="/{role_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role",
    response_description="Role deleted successfully",
)
async def delete_role(
    db_session: DBSession,
    role_service: Annotated[
        RoleService, Depends(dependency=ServiceInitializer(RoleService))
    ],
    role_id: UUID | int,
) -> None:
    """Delete a single role.

    :Description:
    - This route is used to delete a single role by its ID.

    :Args:
    - `role_id` (UUID | int): ID of role to delete. **(Required)**

    :Returns:
    - `None`

    """
    result: bool = role_service.delete_by_id(
        db_session=db_session, record_id=role_id
    )

    if not result:
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": ROLE_NOT_FOUND,
                "data": None,
                "error": None,
            },
        )
