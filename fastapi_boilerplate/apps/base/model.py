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

    Description:
    - This class contains model for message.

    :Attributes:
    - `message` (str): Message.

    """

    message: str


class BasePaginationRead(SQLModel, Generic[Model]):
    """Base Pagination Read Model.

    Description:
    - This class contains base model for pagination.

    :Attributes:
    - `current_page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `next_record_id` (int): ID of first record on next page (None if last
    page)
    - `previous_record_id` (int): ID of first record on previous page (None if
    first page)
    - `records` (Sequence[Model]): List of records for current page.

    """

    current_page: int = Field(default=1, gt=0)
    limit: int = Field(default=10, gt=0)
    total_pages: int = Field(default=0, ge=0)
    total_records: int = Field(default=0, ge=0)
    next_record_id: UUID | int | None = Field(default=None)
    previous_record_id: UUID | int | None = Field(default=None)
    records: Sequence[Model] = Field(default=[])
