"""Base Model.

Description:
- This module contains model for base.

"""

from collections.abc import Sequence
from typing import Generic, TypeVar
from uuid import UUID

from sqlmodel import Field, SQLModel

from fastapi_boilerplate.database.connection import Base

Model = TypeVar("Model", bound=Base)


class Message(SQLModel):
    """Message Model.

    :Description:
    - This class contains model for message.

    :Attributes:
    - `message` (str): Message.

    """

    message: str


class BaseRead(SQLModel, Generic[Model]):
    """Base Read Model.

    :Description:
    - This class contains base model for read.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (Model | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    success: bool = Field(default=True)
    message: str = Field(default="")
    data: Model | None = Field(default=None)
    error: str | None = Field(default=None)


class BasePaginationData(SQLModel, Generic[Model]):
    """Base Pagination Read Model.

    :Description:
    - This class contains base model for pagination.

    :Attributes:
    - `page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `records` (Sequence[Model]): List of records for current page.

    """

    page: int = Field(default=1, gt=0)
    limit: int = Field(default=10, ge=0)
    total_pages: int = Field(default=0, gt=0)
    total_records: int = Field(default=0, ge=0)
    records: Sequence[Model]


class BasePaginationRead(BaseRead[Model]):
    """Base Pagination Read Model.

    :Description:
    - This class contains base model for pagination read.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response
    - `data` (BasePaginationData[Model]): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: BasePaginationData[Model]  # type: ignore[assignment]


class BaseUpdate(SQLModel, Generic[Model]):
    """Base Update Model.

    :Description:
    - This class provides a generic update model for all tables.

    :Attributes:
    - `id` (UUID | int): Unique identifier for the record.
    """

    id: UUID | int
