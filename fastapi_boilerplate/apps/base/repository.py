"""Base Repository Module.

Description:
- This module contains base repository for all repositories in application.

"""

import math
from collections.abc import Sequence
from typing import Generic
from uuid import UUID

from sqlalchemy import ColumnElement
from sqlmodel import SQLModel, col, func, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from fastapi_boilerplate.database.session import DBSession

from .model import BasePaginationData, BaseUpdate, Message, Model


class BaseRepository(Generic[Model]):
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
        self.model: type[Model] = model

    async def create(self, db_session: DBSession, record: SQLModel) -> Model:
        """Create a new record in database.

        :Description:
        - This method adds a new record to database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record` (SQLModel): Model object to be added to database.
        **(Required)**

        :Returns:
        - `record` (Model): Created record.

        """
        db_instance: Model = self.model(**record.model_dump())
        db_session.add(instance=db_instance)
        db_session.commit()
        db_session.refresh(instance=db_instance)

        return db_instance

    async def create_multiple(
        self, db_session: DBSession, records: list[SQLModel]
    ) -> Sequence[Model]:
        """Create multiple records in database.

        :Description:
        - This method adds multiple records to database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[SQLModel]): List of Model objects to be added to
        database. **(Required)**

        :Returns:
        - `records` (Sequence[Model]): List of created records.

        """
        db_instances: list[Model] = [
            self.model(**record.model_dump()) for record in records
        ]
        db_session.add_all(instances=db_instances)
        db_session.commit()

        return db_instances

    async def read_by_id(
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
        return db_session.get(entity=self.model, ident=record_id)

    async def read_multiple_by_ids(
        self, db_session: DBSession, record_ids: list[UUID | int]
    ) -> Sequence[Model]:
        """Retrieve multiple records by their IDs.

        :Description:
        - This method fetches multiple records from database by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `records` (Sequence[Model]): List of retrieved records.

        """
        query: SelectOfScalar[Model] = select(self.model).where(
            col(column_expression=self.model.id).in_(other=record_ids)
        )
        return db_session.exec(statement=query).all()

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
        - This method fetches all records from database and paginates them.
        - It also provides search functionality based on a specific field.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `order_by` (str): Column name to order by. **(Optional)**
        - `desc` (bool): Whether to order in descending order. **(Optional)**
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
        # Validate order column
        order_column: str = order_by or "created_at"

        if not hasattr(self.model, order_column):
            raise ValueError(f"Invalid order column: {order_column}")

        # Validate search column and build search condition
        search_condition: ColumnElement[bool] | None = None

        if search_query and search_by:
            if not hasattr(self.model, search_by):
                raise ValueError(f"Invalid search column: {search_by}")

            search_condition = col(
                column_expression=getattr(self.model, search_by)
            ).contains(other=search_query)

        # Build queries
        count_query: SelectOfScalar[int] = select(
            func.count()  # pylint: disable=not-callable
        ).select_from(self.model)
        main_query: SelectOfScalar[Model] = select(self.model).order_by(
            getattr(self.model, order_column).desc()
            if desc
            else getattr(self.model, order_column)
        )

        if search_condition is not None:
            count_query = count_query.where(search_condition)
            main_query = main_query.where(search_condition)

        # Apply pagination
        if page and limit:
            main_query = main_query.offset(offset=(page - 1) * limit).limit(
                limit=limit
            )

        # Execute queries
        total_records: int = db_session.exec(statement=count_query).one()
        records: Sequence[Model] = db_session.exec(statement=main_query).all()

        return BasePaginationData(
            page=page or 1,
            limit=limit or total_records,
            total_pages=math.ceil(total_records / limit) if limit else 1,
            total_records=total_records,
            records=records,
        )

    async def update_by_id(
        self, db_session: DBSession, record_id: UUID | int, record: SQLModel
    ) -> Model | None:
        """Update a record by its ID.

        :Description:
        - This method updates a record in database by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to update. **(Required)**
        - `record` (SQLModel): Model containing updated fields. **(Required)**

        :Returns:
        - `record` (Model | None): Updated record, or None if not found.

        """
        db_record: Model | None = await self.read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not db_record:
            return None

        db_record.sqlmodel_update(obj=record.model_dump(exclude_unset=True))
        db_session.commit()
        db_session.refresh(instance=db_record)

        return db_record

    async def update_multiple_by_ids(
        self,
        db_session: DBSession,
        records: list[BaseUpdate[Model]],
    ) -> Sequence[Model]:
        """Update multiple records by their IDs.

        :Description:
        - This method updates multiple records in database by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (list[BaseUpdate[Model]]): List of Model objects containing
        updated fields. **(Required)**

        :Returns:
        - `Sequence[Model]`: List of updated records.

        """
        record_ids: list[UUID | int] = [record.id for record in records]

        db_records: Sequence[Model] = await self.read_multiple_by_ids(
            db_session=db_session, record_ids=record_ids
        )

        for db_record, record in zip(db_records, records, strict=False):
            db_record.sqlmodel_update(
                obj=record.model_dump(exclude_unset=True)
            )

        db_session.commit()

        return db_records

    async def delete_by_id(
        self, db_session: DBSession, record_id: UUID | int
    ) -> Message | None:
        """Delete a record by its ID.

        :Description:
        - This method deletes a record from database by its ID.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to delete. **(Required)**

        :Returns:
        - `message` (Message | None): Message indicating that record has been
        deleted, or None if not found.

        """
        record: Model | None = await self.read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not record:
            return None

        db_session.delete(instance=record)
        db_session.commit()

        return Message(message="Record deleted successfully")

    async def delete_multiple_by_ids(
        self, db_session: DBSession, record_ids: list[UUID | int]
    ) -> Message:
        """Delete multiple records by their IDs.

        :Description:
        - This method deletes multiple records from database by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `message` (Message): Message indicating that records have been
        deleted.

        """
        records: Sequence[Model] = await self.read_multiple_by_ids(
            db_session=db_session, record_ids=record_ids
        )

        for record in records:
            db_session.delete(instance=record)

        db_session.commit()

        return Message(message="Records deleted successfully")
