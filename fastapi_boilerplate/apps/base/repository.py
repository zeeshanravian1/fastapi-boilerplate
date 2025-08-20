"""Base Repository Module.

Description:
- This module contains base repository for all repositories in application.

"""

import math
from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import ColumnElement
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel import SQLModel, col, func, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from fastapi_boilerplate.database.connection import Base
from fastapi_boilerplate.database.session import DBSession

from .constant import BASE_ORDER_COLUMN
from .model import BaseBulkUpdate, BasePaginationData, PaginationQueryParams


class BaseRepository[
    Model: Base,
    CreateSchema: SQLModel,
    UpdateSchema: SQLModel,
]:
    """Base Repository Class.

    :Description:
    - This class provides a generic CRUD interface for database models.

    """

    def __init__(self, model: type[Model]) -> None:
        """Initialize BaseRepository.

        :Description:
        - This method initializes BaseRepository with model class.

        :Args:
        - `model` (type[Model]): SQLModel model class to use. **(Required)**

        :Returns:
        - `None`

        """
        self._model: type[Model] = model

    def create(self, db_session: DBSession, record: CreateSchema) -> Model:
        """Create a new record in database.

        :Description:
        - This method adds a new record to database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record` (CreateSchema): Model object to be added to database.
        **(Required)**

        :Returns:
        - `record` (Model): Created record.

        """
        db_instance: Model = self._model(**record.model_dump())
        db_session.add(instance=db_instance)
        db_session.commit()
        db_session.refresh(instance=db_instance)

        return db_instance

    def bulk_create(
        self, db_session: DBSession, records: list[CreateSchema]
    ) -> list[Model]:
        """Create multiple records in database.

        :Description:
        - This method adds multiple records to database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[CreateSchema]): List of Model objects to be added to
        database. **(Required)**

        :Returns:
        - `records` (list[Model]): List of created records.

        """
        db_instances: list[Model] = [
            self._model(**record.model_dump()) for record in records
        ]
        db_session.add_all(instances=db_instances)
        db_session.commit()

        return db_instances

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
        return db_session.get(entity=self._model, ident=record_id)

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
        query: SelectOfScalar[Model] = select(self._model).where(
            col(column_expression=self._model.id).in_(other=record_ids)
        )

        return list(db_session.exec(statement=query).all())

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
        query: SelectOfScalar[Model] = select(self._model).where(
            col(column_expression=getattr(self._model, field)) == value
        )

        return db_session.exec(statement=query).one_or_none()

    def read_by_bulk_fields(
        self,
        db_session: DBSession,
        fields: list[
            tuple[
                str, int | UUID | float | str | bool | datetime | PhoneNumber
            ]
        ],
    ) -> Model | None:
        """Retrieve a single record by multiple fields.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `fields` (list[tuple[str, int | UUID | float | str | bool | datetime]
        ]): List of field-value pairs to filter by. **(Required)**

        :Returns:
        - `record` (Model | None): Retrieved record, or None if not found.

        """
        query: SelectOfScalar[Model] = select(self._model).where(
            *[
                col(column_expression=getattr(self._model, field)) == value
                for field, value in fields
            ]
        )

        return db_session.exec(statement=query).one_or_none()

    def read_all(
        self,
        db_session: DBSession,
        params: PaginationQueryParams = PaginationQueryParams(),
    ) -> BasePaginationData[Model]:
        """Retrieve all records with pagination.

        :Description:
        - This method fetches all records from database and paginates them.
        - It also provides search functionality based on a specific field.

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
        # Validate order column
        order_column: str = params.order_by or BASE_ORDER_COLUMN

        if not hasattr(self._model, order_column):
            raise ValueError(f"Invalid order column: {order_column}")

        # Build base queries
        count_query: SelectOfScalar[int] = select(
            func.count()  # pylint: disable=not-callable
        ).select_from(self._model)
        main_query: SelectOfScalar[Model] = select(self._model)

        # Apply search filter if provided
        if params.search_by and params.search_query:
            if not hasattr(self._model, params.search_by):
                raise ValueError(f"Invalid search column: {params.search_by}")

            search_filter: ColumnElement[bool] = col(
                column_expression=getattr(self._model, params.search_by)
            ).contains(other=params.search_query)

            count_query = count_query.where(search_filter)
            main_query = main_query.where(search_filter)

        # Apply ordering and pagination
        order_attr: InstrumentedAttribute[int | UUID | float | str | bool] = (
            getattr(self._model, order_column)
        )

        main_query = main_query.order_by(
            order_attr.desc() if params.desc else order_attr
        )
        main_query = main_query.offset(
            offset=(params.page - 1) * params.limit
        ).limit(limit=params.limit)

        # Execute queries
        total_records: int = db_session.exec(statement=count_query).one()
        records: list[Model] = list(
            db_session.exec(statement=main_query).all()
        )

        return BasePaginationData(
            page=params.page,
            limit=params.limit,
            total_pages=(
                math.ceil(total_records / params.limit)
                if params.limit > 0
                else 1
            ),
            total_records=total_records,
            records=records,
        )

    def update_by_id(
        self,
        db_session: DBSession,
        record_id: UUID | int,
        record: UpdateSchema,
    ) -> Model | None:
        """Update a record by its ID.

        :Description:
        - This method updates a record in database by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to update. **(Required)**
        - `record` (UpdateSchema): Model containing updated fields.
        **(Required)**

        :Returns:
        - `record` (Model | None): Updated record, or None if not found.

        """
        db_record: Model | None = self.read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not db_record:
            return None

        db_record.sqlmodel_update(obj=record.model_dump(exclude_unset=True))
        db_session.commit()
        db_session.refresh(instance=db_record)

        return db_record

    def update_bulk_by_ids(
        self,
        db_session: DBSession,
        records: Sequence[BaseBulkUpdate],
    ) -> list[Model]:
        """Update multiple records by their IDs.

        :Description:
        - This method updates multiple records by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[BaseBulkUpdate]): List of Model objects
        containing updated fields. **(Required)**

        :Returns:
        - `list[Model]`: List of updated records.

        """
        record_ids: list[UUID | int] = [record.id for record in records]

        db_records: list[Model] = self.read_bulk_by_ids(
            db_session=db_session, record_ids=record_ids
        )

        for db_record, record in zip(db_records, records, strict=False):
            db_record.sqlmodel_update(
                obj=record.model_dump(exclude_unset=True, exclude={"id"})
            )

        db_session.commit()

        return db_records

    def delete_by_id(
        self, db_session: DBSession, record_id: UUID | int
    ) -> bool:
        """Delete a record by its ID.

        :Description:
        - This method deletes a record from database by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to delete. **(Required)**

        :Returns:
        - `bool`: True if record was deleted, False if not found.

        """
        record: Model | None = self.read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not record:
            return False

        db_session.delete(instance=record)
        db_session.commit()

        return True

    def delete_bulk_by_ids(
        self, db_session: DBSession, record_ids: list[UUID | int]
    ) -> None:
        """Delete multiple records by their IDs.

        :Description:
        - This method deletes multiple records from database by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `None`

        """
        records: list[Model] = self.read_bulk_by_ids(
            db_session=db_session, record_ids=record_ids
        )

        for record in records:
            db_session.delete(instance=record)

        db_session.commit()
