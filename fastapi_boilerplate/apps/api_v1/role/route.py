"""Role Route Module.

Description:
- This module is responsible for handling role routes.

"""

from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse

from fastapi_boilerplate.apps.api_v1.role.service import RoleService
from fastapi_boilerplate.apps.base.model import BasePaginationData, Message
from fastapi_boilerplate.database.session import DBSession

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
    RoleUpdate,
)

router = APIRouter(prefix="/role", tags=["Role"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single role",
    response_description="Role created successfully",
)
async def create_role(
    db_session: DBSession,
    record: RoleCreate,
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleRead:
    """Create a single role.

    :Description:
    - This route is used to create a single role.

    :Args:
    Role details to be created with following fields:
    - `role_name` (str): Name of role. **(Required)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    Role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    result: Role = await role_service.create(
        db_session=db_session, record=record
    )

    return RoleRead(
        success=True,
        message="Role created successfully",
        data=Role.model_validate(obj=result),
    )


@router.post(
    path="/bulk",
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple roles",
    response_description="Roles created successfully",
)
async def create_roles(
    db_session: DBSession,
    records: list[RoleCreate],
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleBulkRead:
    """Create multiple roles.

    :Description:
    - This route is used to create multiple roles.

    :Args:
    List of role details to be created with following fields:
    - `role_name` (str): Name of role. **(Required)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    List of role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    results: Sequence[Role] = await role_service.create_multiple(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return RoleBulkRead(
        success=True,
        message="Roles created successfully",
        data=[Role.model_validate(obj=result) for result in results],
    )


@router.get(
    path="/bulk",
    status_code=status.HTTP_200_OK,
    summary="Retrieve multiple roles by IDs",
    response_description="Roles retrieved successfully",
)
async def read_roles_by_ids(
    db_session: DBSession,
    role_ids: Annotated[list[UUID], Query(...)],
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleBulkRead:
    """Retrieve multiple roles by IDs.

    :Description:
    - This route is used to retrieve multiple roles by their IDs.

    :Args:
    - `role_ids` (list[UUID]): List of role IDs. **(Required)**

    :Returns:
    List of role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    results: Sequence[Role] = await role_service.read_multiple_by_ids(
        db_session=db_session,
        record_ids=role_ids,  # type: ignore[arg-type]
    )

    return RoleBulkRead(
        success=True,
        message="Roles retrieved successfully",
        data=[Role.model_validate(obj=result) for result in results],
    )


@router.get(
    path="/{role_id}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single role by ID",
    response_description="Role retrieved successfully",
)
async def read_role_by_id(
    db_session: DBSession,
    role_id: Annotated[UUID, "Role ID"],
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleRead:
    """Retrieve a single role by ID.

    :Description:
    - This route is used to retrieve a single role by its ID.

    :Args:
    - `role_id` (UUID): ID of role. **(Required)**

    :Returns:
    Role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    result: Role | None = await role_service.read_by_id(
        db_session=db_session, record_id=role_id
    )

    if not isinstance(result, Role):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Role not found",
                "data": None,
            },
        )

    return RoleRead(
        success=True,
        message="Role retrieved successfully",
        data=Role.model_validate(obj=result),
    )


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Retrieve all roles",
    response_description="Roles retrieved successfully",
)
async def read_roles(
    db_session: DBSession,
    order_by: str | None = None,
    desc: bool = False,
    page: int | None = None,
    limit: int | None = None,
    search_by: str | None = None,
    search_query: str | None = None,
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RolePaginationRead:
    """Retrieve all roles.

    :Description:
    - This route is used to retrieve all roles.

    :Returns:
    List of role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    results: BasePaginationData[Role] = await role_service.read_all(
        db_session=db_session,
        order_by=order_by,
        desc=desc,
        page=page,
        limit=limit,
        search_by=search_by,
        search_query=search_query,
    )

    return RolePaginationRead(
        success=True,
        message="Roles retrieved successfully",
        data=RolePaginationData.model_validate(obj=results),
    )


@router.put(
    path="/{role_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single role by ID",
    response_description="Role updated successfully",
)
async def update_role_by_id(
    db_session: DBSession,
    role_id: Annotated[UUID, "Role ID"],
    record: RoleUpdate,
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleRead:
    """Update a single role by ID.

    :Description:
    - This route is used to update a single role by its ID.

    :Args:
    - `role_id` (UUID): ID of role. **(Required)**
    Role details to be updated with following fields:
    - `role_name` (str): Name of role. **(Optional)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    Role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    result: Role | None = await role_service.update_by_id(
        db_session=db_session, record_id=role_id, record=record
    )

    if not isinstance(result, Role):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Role not found",
                "data": None,
            },
        )

    return RoleRead(
        success=True,
        message="Role updated successfully",
        data=Role.model_validate(obj=result),
    )


@router.put(
    path="/bulk",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update multiple roles by IDs",
    response_description="Roles updated successfully",
)
async def update_roles_by_ids(
    db_session: DBSession,
    records: list[RoleBulkUpdate],
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleBulkRead:
    """Update multiple roles by IDs.

    :Description:
    - This route is used to update multiple roles by their IDs.

    :Args:
    List of role details to be updated with following fields:
    - `id` (UUID): Id of role. **(Required)**
    - `role_name` (str): Name of role. **(Optional)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    List of role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    results: Sequence[Role] = await role_service.update_multiple_by_ids(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return RoleBulkRead(
        success=True,
        message="Roles updated successfully",
        data=[Role.model_validate(obj=result) for result in results],
    )


@router.patch(
    path="/{role_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Patch a single role by ID",
    response_description="Role patched successfully",
)
async def patch_role_by_id(
    db_session: DBSession,
    role_id: Annotated[UUID, "Role ID"],
    record: RolePatch,
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleRead:
    """Patch a single role by ID.

    :Description:
    - This route is used to patch a single role by its ID.

    :Args:
    - `role_id` (UUID): ID of role. **(Required)**
    Role details to be patched with following fields:
    - `role_name` (str): Name of role. **(Optional)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    Role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    result: Role | None = await role_service.update_by_id(
        db_session=db_session, record_id=role_id, record=record
    )

    if not isinstance(result, Role):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Role not found",
                "data": None,
            },
        )

    return RoleRead(
        success=True,
        message="Role patched successfully",
        data=Role.model_validate(obj=result),
    )


@router.patch(
    path="/bulk",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Patch multiple roles by IDs",
    response_description="Roles patched successfully",
)
async def patch_roles_by_ids(
    db_session: DBSession,
    records: list[RoleBulkPatch],
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> RoleBulkRead:
    """Patch multiple roles by IDs.

    :Description:
    - This route is used to patch multiple roles by their IDs.

    :Args:
    List of role details to be patched with following fields:
    - `id` (UUID): Id of role. **(Required)**
    - `role_name` (str): Name of role. **(Optional)**
    - `role_description` (str): Description of role. **(Optional)**

    :Returns:
    List of role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    results: Sequence[Role] = await role_service.update_multiple_by_ids(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return RoleBulkRead(
        success=True,
        message="Roles patched successfully",
        data=[Role.model_validate(obj=result) for result in results],
    )


@router.delete(
    path="/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single role by ID",
    response_description="Role deleted successfully",
)
async def delete_role_by_id(
    db_session: DBSession,
    role_id: Annotated[UUID, "Role ID"],
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> None:
    """Delete a single role by ID.

    :Description:
    - This route is used to delete a single role by its ID.

    :Args:
    - `role_id` (UUID): ID of role. **(Required)**

    :Returns:
    Role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    result: Message | None = await role_service.delete_by_id(
        db_session=db_session, record_id=role_id
    )

    if not isinstance(result, Message):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Role not found",
                "data": None,
            },
        )


@router.delete(
    path="/bulk",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete multiple roles by IDs",
    response_description="Roles deleted successfully",
)
async def delete_roles_by_ids(
    db_session: DBSession,
    role_ids: Annotated[list[UUID], Query(...)],
    role_service: RoleService = Depends(lambda: RoleService(model=Role)),
) -> None:
    """Delete multiple roles by IDs.

    :Description:
    - This route is used to delete multiple roles by their IDs.

    :Args:
    - `role_ids` (list[UUID]): List of role IDs. **(Required)**

    :Returns:
    Role details along with following information:
    - `id` (UUID): Id of role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Datetime of role creation.
    - `updated_at` (datetime): Datetime of role updation.

    """
    result: Message | None = await role_service.delete_multiple_by_ids(
        db_session=db_session,
        record_ids=role_ids,  # type: ignore[arg-type]
    )

    if not isinstance(result, Message):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Roles not found",
                "data": None,
            },
        )
