"""Base Service Module.

Description:
- This module contains base service for all services in application.

"""

from collections.abc import Sequence
from typing import Generic
from uuid import UUID

from sqlmodel import SQLModel

from fastapi_boilerplate.database.session import DBSession

from .model import BasePaginationData, BaseUpdate, Message, Model
from .repository import BaseRepository


class BaseService(Generic[Model]):
    """Base Service Class.

    :Description:
    - This class provides a generic CRUD interface for for services.

    """

    def __init__(self, model: type[Model]) -> None:
        """Initialize BaseService.

        :Description:
        - This method initializes BaseService with model class.

        :Args:
        - `model` (type[Model]): SQLModel model class to use. **(Required)**

        :Returns:
        - `None`

        """
        self.repository = BaseRepository[Model](model=model)

    async def create(self, db_session: DBSession, record: SQLModel) -> Model:
        """Create a new record.

        :Description:
        - This method creates a new record.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record` (SQLModel): Model object to be added to database.
        **(Required)**

        :Returns:
        - `record` (Model): Created record.

        """
        return await self.repository.create(
            db_session=db_session, record=record
        )

    async def create_multiple(
        self, db_session: DBSession, records: list[SQLModel]
    ) -> Sequence[Model]:
        """Create multiple records.

        :Description:
        - This method creates multiple records.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[SQLModel]): List of Model objects to be added to
        database. **(Required)**

        :Returns:
        - `records` (list[Model]): List of created records.

        """
        return await self.repository.create_multiple(
            db_session=db_session, records=records
        )

    async def read_by_id(
        self, db_session: DBSession, record_id: UUID | int
    ) -> Model | None:
        """Retrieve a single record by its ID.

        :Description:
        - This method retrieves a single record by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record. **(Required)**

        :Returns:
        - `record` (Model | None): Retrieved record, or None if not found.

        """
        return await self.repository.read_by_id(
            db_session=db_session, record_id=record_id
        )

    async def read_multiple_by_ids(
        self, db_session: DBSession, record_ids: list[UUID | int]
    ) -> Sequence[Model]:
        """Retrieve multiple records by their IDs.

        :Description:
        - This method retrieves multiple records by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `records` (Sequence[Model]): List of retrieved records.

        """
        return await self.repository.read_multiple_by_ids(
            db_session=db_session, record_ids=record_ids
        )

    async def read_all(
        self,
        db_session: DBSession,
        order_by: str | None = None,
        desc: bool = False,
        page: int | None = None,
        limit: int | None = None,
        search_by: str | None = None,
        search_query: str | None = None,
    ) -> BasePaginationData[Model]:
        """Retrieve all records.

        :Description:
        - This method fetches all records and paginates them.
        - It also provides search functionality based on a specific field.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `page` (int): Page number to fetch. **(Optional)**
        - `limit` (int): Number of records per page. **(Optional)**
        - `search_by` (str): Field to search by. **(Optional)**
        - `search_query` (str): Query string for search. **(Optional)**

        :Returns:
        - `PaginationBase`: Paginated records along with following details:
            - `page` (int): Current page number.
            - `limit` (int): Number of records per page.
            - `total_pages` (int): Total number of pages.
            - `total_records` (int): Total number of records.
            - `records` (Sequence[Model]): List of records for current page.

        """
        return await self.repository.read_all(
            db_session=db_session,
            order_by=order_by,
            desc=desc,
            page=page,
            limit=limit,
            search_by=search_by,
            search_query=search_query,
        )

    async def update_by_id(
        self, db_session: DBSession, record_id: UUID | int, record: SQLModel
    ) -> Model | None:
        """Update a record by its ID.

        :Description:
        - This method updates a record by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to update. **(Required)**
        - `record` (SQLModel): Model containing updated fields. **(Required)**

        :Returns:
        - `record` (Model | None): Updated record, or None if not found.

        """
        return await self.repository.update_by_id(
            db_session=db_session, record_id=record_id, record=record
        )

    async def update_multiple_by_ids(
        self,
        db_session: DBSession,
        records: list[BaseUpdate[Model]],
    ) -> Sequence[Model]:
        """Update multiple records by their IDs.

        :Description:
        - This method updates multiple records by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[SQLModel]): List of Model objects containing
        updated fields. **(Required)**

        :Returns:
        - `Sequence[Model]`: List of updated records.

        """
        return await self.repository.update_multiple_by_ids(
            db_session=db_session, records=records
        )

    async def delete_by_id(
        self, db_session: DBSession, record_id: UUID | int
    ) -> Message | None:
        """Delete a record by its ID.

        :Description:
        - This method deletes a record by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to delete. **(Required)**

        :Returns:
        - `message` (Message | None): Message indicating that record has been
        deleted, or None if not found.

        """
        return await self.repository.delete_by_id(
            db_session=db_session, record_id=record_id
        )

    async def delete_multiple_by_ids(
        self, db_session: DBSession, record_ids: list[UUID | int]
    ) -> Message | None:
        """Delete multiple records by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `message` (Message): Message indicating that records have been
        deleted.

        """
        return await self.repository.delete_multiple_by_ids(
            db_session=db_session, record_ids=record_ids
        )
