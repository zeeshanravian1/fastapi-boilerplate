"""Base Service Module.

Description:
- This module contains base service for all services in application.

"""

from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel

from fastapi_boilerplate.database.connection import Base
from fastapi_boilerplate.database.session import DBSession

from .model import BaseBulkUpdate, BasePaginationData, PaginationQueryParams
from .repository import BaseRepository


class BaseService[
    Model: Base,
    CreateSchema: SQLModel,
    UpdateSchema: SQLModel,
]:
    """Base Service Class.

    :Description:
    - This class provides a generic CRUD interface for services.

    """

    def __init__(
        self, repository: BaseRepository[Model, CreateSchema, UpdateSchema]
    ) -> None:
        """Initialize BaseService.

        :Description:
        - This method initializes BaseService with repository instance.

        :Args:
        - `repository` (BaseRepository): Repository instance to use.
        **(Required)**

        :Returns:
        - `None`

        """
        self.repository: BaseRepository[Model, CreateSchema, UpdateSchema] = (
            repository
        )

    def create(self, db_session: DBSession, record: CreateSchema) -> Model:
        """Create a new record.

        :Description:
        - This method creates a new record in database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record` (CreateSchema): Model object to be added to database.
        **(Required)**

        :Returns:
        - `record` (Model): Created record.

        """
        return self.repository.create(db_session=db_session, record=record)

    def bulk_create(
        self, db_session: DBSession, records: list[CreateSchema]
    ) -> list[Model]:
        """Create multiple records.

        :Description:
        - This method creates multiple records in database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[CreateSchema]): List of Model objects to be added to
        database. **(Required)**

        :Returns:
        - `records` (list[Model]): List of created records.

        """
        return self.repository.bulk_create(
            db_session=db_session, records=records
        )

    def read_by_id(
        self, db_session: DBSession, record_id: UUID | int
    ) -> Model | None:
        """Retrieve a single record by its ID.

        :Description:
        - This method fetches a single record from database by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record. **(Required)**

        :Returns:
        - `record` (Model | None): Retrieved record, or None if not found.

        """
        return self.repository.read_by_id(
            db_session=db_session, record_id=record_id
        )

    def read_bulk_by_ids(
        self, db_session: DBSession, record_ids: list[UUID | int]
    ) -> list[Model]:
        """Retrieve multiple records by their IDs.

        :Description:
        - This method fetches multiple records from database by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `records` (list[Model]): List of retrieved records.

        """
        return self.repository.read_bulk_by_ids(
            db_session=db_session, record_ids=record_ids
        )

    def read_by_field(
        self,
        db_session: DBSession,
        field: str,
        value: int | UUID | float | str | bool | datetime,
    ) -> Model | None:
        """Retrieve a single record by a specific field.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `field` (str): Field name to filter by. **(Required)**
        - `value` (int | UUID | float | str | bool | datetime): Value to match
        for specified field. **(Required)**

        :Returns:
        - `record` (Model | None): Retrieved record, or None if not found.

        """
        return self.repository.read_by_field(
            db_session=db_session, field=field, value=value
        )

    def read_by_bulk_fields(
        self,
        db_session: DBSession,
        fields: list[tuple[str, int | UUID | float | str | bool | datetime]],
    ) -> Model | None:
        """Retrieve a single record by multiple fields.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `fields` (list[tuple[str, int | UUID | float | str | bool | datetime]
        ]): List of field-value pairs to filter by. **(Required)**

        :Returns:
        - `record` (Model | None): Retrieved record, or None if not found.

        """
        return self.repository.read_by_bulk_fields(
            db_session=db_session, fields=fields
        )

    def read_all(
        self,
        db_session: DBSession,
        params: PaginationQueryParams = PaginationQueryParams(),
    ) -> BasePaginationData[Model]:
        """Retrieve all records with pagination.

        :Description:
        - This method fetches all records with pagination and search.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**

        - `params` (PaginationQueryParams): Query parameters for pagination,
        ordering and search with following attributes:
            - `page` (int): Page number for pagination. **(Optional)**
            - `limit` (int): Number of records per page. **(Optional)**
            - `order_by` (str | None): Field to order by. **(Optional)**
            - `desc` (bool): Whether to order in descending. **(Optional)**
            - `search_by` (str | None): Field to search by. **(Optional)**
            - `search_query` (str | None): Search query string. **(Optional)**

        :Returns:
        - `BasePaginationData[Model]`: Paginated records with following
        attributes:
            - `page` (int): Current page number.
            - `limit` (int): Number of records per page.
            - `total_pages` (int): Total number of pages.
            - `total_records` (int): Total number of records.
            - `records` (list[Model]): List of records for current page.

        """
        return self.repository.read_all(db_session=db_session, params=params)

    def update_by_id(
        self,
        db_session: DBSession,
        record_id: UUID | int,
        record: UpdateSchema,
    ) -> Model | None:
        """Update a record by its ID.

        :Description:
        - This method updates a record in database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to update. **(Required)**
        - `record` (UpdateSchema): Model containing updated fields.
        **(Required)**

        :Returns:
        - `record` (Model | None): Updated record, or None if not found.

        """
        return self.repository.update_by_id(
            db_session=db_session, record_id=record_id, record=record
        )

    def update_bulk_by_ids(
        self,
        db_session: DBSession,
        records: Sequence[BaseBulkUpdate],
    ) -> list[Model]:
        """Update multiple records by their IDs.

        :Description:
        - This method updates multiple records in database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[tuple[UUID | int, UpdateSchema]]): List of tuples
        containing record ID and update data. **(Required)**

        :Returns:
        - `list[Model]`: List of updated records.

        """
        return self.repository.update_bulk_by_ids(
            db_session=db_session, records=records
        )

    def delete_by_id(
        self, db_session: DBSession, record_id: UUID | int
    ) -> bool:
        """Delete a record by its ID.

        :Description:
        - This method deletes a record from database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to delete. **(Required)**

        :Returns:
        - `bool`: True if record was deleted, False if not found.

        """
        return self.repository.delete_by_id(
            db_session=db_session, record_id=record_id
        )

    def delete_bulk_by_ids(
        self, db_session: DBSession, record_ids: list[UUID | int]
    ) -> None:
        """Delete multiple records by their IDs.

        :Description:
        - This method deletes multiple records from database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `None`

        """
        self.repository.delete_bulk_by_ids(
            db_session=db_session, record_ids=record_ids
        )
