"""Role Model.

Description:
- This module contains role models.

"""

from collections.abc import Sequence

from sqlmodel import Field, SQLModel

from fastapi_boilerplate.apps.base.model import (
    BasePaginationData,
    BasePaginationRead,
    BaseRead,
    BaseUpdate,
)
from fastapi_boilerplate.database.connection import Base


class RoleBase(SQLModel):
    """Role Base Model.

    :Description:
    - This class contains base model for role table.

    :Attributes:
    - `role_name` (str): Name of role.
    - `role_description` (str | None): Description of role.

    """

    role_name: str = Field(
        min_length=1, max_length=255, schema_extra={"examples": ["admin"]}
    )
    role_description: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["Admin Role"]},
    )


class Role(Base, RoleBase, table=True):
    """Role Table.

    :Description:
    - This class contains model for role table.

    :Attributes:
    - `id` (UUID): Unique identifier for role.
    - `role_name` (str): Name of role.
    - `role_description` (str): Description of role.
    - `created_at` (datetime): Timestamp when role was created.
    - `updated_at` (datetime): Timestamp when role was last updated.

    """


class RoleCreate(RoleBase):
    """Role Create Model.

    :Description:
    - This class contains model for creating role.

    :Attributes:
    - `role_name` (str): Name of role.
    - `role_description` (str | None): Description of role.

    """


class RoleRead(BaseRead[Role]):
    """Role Read Model.

    :Description:
    - This class contains model for reading role.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (Role | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: Role | None = Field(default=None)


class RoleBulkRead(BaseRead[Role]):
    """Role Bulk Read Model.

    :Description:
    - This class contains model for bulk reading role.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (list[Role]): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: Sequence[Role]  # type: ignore[assignment]


class RolePaginationData(BasePaginationData[Role]):
    """Role Pagination Read Model.

    :Description:
    - This class contains model for pagination reading role.

    :Attributes:
    - `page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `records` (Sequence[Role]): List of records for current page.

    """

    records: Sequence[Role]


class RolePaginationRead(BasePaginationRead[Role]):
    """Role Pagination Read Model.

    :Description:
    - This class contains model for pagination reading role.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (RolePaginationData | None): Data for response.
    - `error` (str | None): Error message

    """

    data: RolePaginationData  # type: ignore[assignment]


class RoleUpdate(RoleBase):
    """Role Update Model.

    :Description:
    - This class contains model for updating role.

    :Attributes:
    - `role_name` (str | None): Name of role.
    - `role_description` (str | None): Description of role.

    """


class RoleBulkUpdate(BaseUpdate[Role], RoleUpdate):
    """Role Bulk Update Model.

    :Description:
    - This class contains model for bulk updating role.

    :Attributes:
    - `id` (UUID | int): Unique identifier for role.
    - `role_name` (str | None): Name of role.
    - `role_description` (str | None): Description of role.

    """


class RolePatch(RoleBase):
    """Role Patch Model.

    :Description:
    - This class contains model for patching role.

    :Attributes:
    - `role_name` (str | None): Name of role.
    - `role_description` (str | None): Description of role.

    """

    role_name: str | None = None  # type: ignore[assignment]


class RoleBulkPatch(BaseUpdate[Role], RolePatch):
    """Role Bulk Patch Model.

    :Description:
    - This class contains model for bulk patching role.

    :Attributes:
    - `id` (UUID | int): Unique identifier for role.
    - `role_name` (str | None): Name of role.
    - `role_description` (str | None): Description of role.

    """
