"""Role Model.

Description:
- This module contains role models.

"""

from collections.abc import Sequence

from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig

from fastapi_boilerplate.apps.base.model import (
    BaseBulkUpdate,
    BasePaginationData,
    BasePaginationRead,
    BaseRead,
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
        min_length=1,
        max_length=255,
        unique=True,
        schema_extra={"examples": ["admin"]},
    )
    role_description: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["Admin Role"]},
    )

    # Settings Configuration
    model_config = SQLModelConfig(
        str_strip_whitespace=True,  # type: ignore[unused-ignore]
    )


class Role(Base, RoleBase, table=True):
    """Role Table.

    :Description:
    - This class contains model for role table.

    :Attributes:
    - `id` (UUID | int): Unique identifier for role.
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
    - This class contains model for reading multiple roles.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (list[Role]): List of roles.
    - `error` (str | None): Error message if any.

    """

    data: list[Role]  # type: ignore[assignment]


class RolePaginationData(BasePaginationData[Role]):
    """Role Pagination Data Model.

    :Description:
    - This class contains model for paginated reading of roles.

    :Attributes:
    - `page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `records` (Sequence[Role]): List of role records for current
    page.

    """

    records: Sequence[Role]


class RolePaginationRead(BasePaginationRead[Role]):
    """Role Pagination Read Model.

    :Description:
    - This class contains model for paginated reading of roles.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (BasePaginationData[Role]): Paginated data for response.
    - `error` (str | None): Error message if any.

    """

    data: RolePaginationData  # type: ignore[unused-ignore]


class RoleUpdate(RoleBase):
    """Role Update Model.

    :Description:
    - This class contains model for updating role.

    :Attributes:
    - `role_name` (str): Name of role.
    - `role_description` (str | None): Description of role.

    """


class RoleBulkUpdate(BaseBulkUpdate, RoleUpdate):
    """Role Bulk Update Model.

    :Description:
    - This class contains model for bulk updating roles.

    :Attributes:
    - `data` (list[RoleUpdate]): List of roles to be updated.
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `error` (str | None): Error message if any.

    """


class RolePatch(RoleBase):
    """Role Patch Model.

    :Description:
    - This class contains model for patching role.

    :Attributes:
    - `role_name` (str | None): Name of role.
    - `role_description` (str | None): Description of role.

    """

    role_name: str | None = Field(  # type: ignore[assignment]
        default=None,
        min_length=1,
        max_length=255,
        unique=True,
        schema_extra={"examples": ["admin"]},
    )


class RoleBulkPatch(BaseBulkUpdate, RolePatch):
    """Role Bulk Patch Model.

    :Description:
    - This class contains model for bulk patching roles.

    :Attributes:
    - `data` (list[RolePatch]): List of roles to be patched.
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `error` (str | None): Error message if any.

    """
