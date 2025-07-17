"""Base Model.

Description:
- This module contains model for base.

"""

from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from sqlmodel import Field, SQLModel


@dataclass
class PaginationQueryParams:
    """Query Parameters for Pagination.

    :Description:
    - This class contains query parameters for pagination.

    :Attributes:
    - `page` (int): Page number for pagination.
    - `limit` (int): Number of records per page.
    - `order_by` (str | None): Field to order by.
    - `desc` (bool): Whether to order in descending order.
    - `search_by` (str | None): Field to search by.
    - `search_query` (str | None): Search query string.

    """

    page: int = 1
    limit: int = 10
    order_by: str | None = None
    desc: bool = False
    search_by: str | None = None
    search_query: str | None = None


class BaseRead[T: SQLModel](SQLModel):
    """Base Read Model.

    :Description:
    - This class contains base model for read.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (T | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    success: bool = Field(default=True)
    message: str = Field(default="")
    data: T | None = Field(default=None)
    error: str | list[dict[str, str]] | None = Field(default=None)


class BasePaginationData[T: SQLModel](SQLModel):
    """Base Pagination Data Model.

    :Description:
    - This class contains base model for pagination data.

    :Attributes:
    - `page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `records` (Sequence[T]): List of records for current page.

    """

    page: int = Field(default=1, gt=0)
    limit: int = Field(default=10, ge=1)
    total_pages: int = Field(default=0, ge=0)
    total_records: int = Field(default=0, ge=0)
    records: Sequence[T]


class BasePaginationRead[T: SQLModel](SQLModel):
    """Base Pagination Read Model.

    :Description:
    - This class contains base model for pagination read.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response
    - `data` (BasePaginationData[T]): Data for response.
    - `error` (str | None): Error message if any.

    """

    success: bool = Field(default=True)
    message: str = Field(default="")
    data: BasePaginationData[T]
    error: str | None = Field(default=None)


class BaseBulkUpdate(SQLModel):
    """Base Update Model.

    :Description:
    - This class provides a generic bulk update model for all tables.

    :Attributes:
    - `id` (UUID | int): Unique identifier for record.

    """

    id: UUID | int
