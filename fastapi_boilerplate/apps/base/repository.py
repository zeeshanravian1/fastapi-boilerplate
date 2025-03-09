"""Base View Module.

Description:
- This module contains base view for all views in application.

"""

from collections.abc import Sequence
from typing import Generic
from uuid import UUID

from sqlalchemy import ColumnElement
from sqlmodel import SQLModel, col, func, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from fastapi_boilerplate.database.session import DBSession

from .model import BasePaginationRead, Message, Model


class BaseView(Generic[Model]):
    """Base View Class.

    Description:
    - This class provides a generic CRUD interface for database models.

    """

    def __init__(self, model: type[Model]) -> None:
        """Initialize BaseView.

        :Args:
        - `model` (type[Model]): SQLModel model class. **(Required)**

        :Returns:
        - `None`

        """
        self.model: type[Model] = model

    async def create(self, db_session: DBSession, record: SQLModel) -> Model:
        """Create a new record in database.

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
        self, db_session: DBSession, records: Sequence[SQLModel]
    ) -> Sequence[Model]:
        """Create multiple records in database.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `records` (Sequence[SQLModel]): List of Model objects to be added to
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
        page: int = 1,
        limit: int = 10,
        search_by: str | None = None,
        search_query: str | None = None,
    ) -> BasePaginationRead[Model]:
        """Retrieve all records.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `page` (int): Page number to fetch. **(Optional)**
        - `limit` (int): Number of records per page. **(Optional)**
        - `search_by` (str): Field to search by. **(Optional)**
        - `search_query` (str): Query string for search. **(Optional)**

        :Returns:
        - `PaginationBase`: Paginated records along with following details:
            - `current_page` (int): Current page number.
            - `limit` (int): Number of records per page.
            - `total_pages` (int): Total number of pages.
            - `total_records` (int): Total number of records.
            - `next_record_id` (int): ID of first record on next page (None if
            last page)
            - `previous_record_id` (int): ID of first record on previous page
            (None if first page)
            - `records` (Sequence[Model]): List of records for current page.

        """
        # Validate search column and build search condition
        search_condition: ColumnElement[bool] | None = None

        if search_by:
            if not hasattr(self.model, search_by):
                raise ValueError("Invalid search column")

            if search_query:
                search_condition = col(
                    column_expression=getattr(self.model, search_by)
                ).contains(other=search_query)

        # Count total records and build base query
        count_query: SelectOfScalar[int] = select(
            func.count()  # pylint: disable=not-callable
        ).select_from(self.model)
        base_query: SelectOfScalar[UUID] = select(self.model.id).order_by(
            self.model.created_at  # type: ignore[arg-type]
        )
        main_query: SelectOfScalar[Model] = select(self.model).order_by(
            self.model.created_at  # type: ignore[arg-type]
        )

        # Apply search condition to all queries if needed
        if search_condition is not None:
            count_query = count_query.where(search_condition)
            base_query = base_query.where(search_condition)
            main_query = main_query.where(search_condition)

        # Get total count and calculate pages
        total_records: int = db_session.exec(statement=count_query).one()
        total_pages: int = max(1, (total_records + limit - 1) // limit)
        page = max(1, page)  # Ensure page is at least 1

        # Initialize pagination variables
        offset: int = (page - 1) * limit
        records: Sequence[Model] = []
        next_record_id: UUID | int | None = None
        previous_record_id: UUID | int | None = None

        if (
            page > total_pages
            and page == total_pages + 1
            and total_records > 0
        ):
            prev_offset: int = (total_pages - 1) * limit
            previous_record_id = db_session.exec(
                statement=base_query.offset(offset=prev_offset).limit(limit=1)
            ).first()

        elif page <= total_pages and total_records > 0:
            # Fetch current page records
            records = db_session.exec(
                statement=main_query.offset(offset=offset).limit(limit=limit)
            ).all()

            # Set previous_record_id if not on first page
            if page > 1:
                prev_offset = (page - 2) * limit
                previous_record_id = db_session.exec(
                    statement=base_query.offset(offset=prev_offset).limit(
                        limit=1
                    )
                ).first()

            # Set next_record_id if not on last page
            if page < total_pages:
                next_offset: int = page * limit
                next_record_id = db_session.exec(
                    statement=base_query.offset(offset=next_offset).limit(
                        limit=1
                    )
                ).first()

        # Create and return pagination result
        return BasePaginationRead(
            current_page=page,
            limit=limit,
            total_pages=total_pages,
            total_records=total_records,
            next_record_id=next_record_id,
            previous_record_id=previous_record_id,
            records=records,
        )

    async def update_by_id(
        self, db_session: DBSession, record_id: UUID | int, record: SQLModel
    ) -> Model | None:
        """Update a record by its ID.

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
        record_ids: list[UUID | int],
        records: Sequence[SQLModel],
    ) -> Sequence[Model]:
        """Update multiple records by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**
        - `records` (Sequence[SQLModel]): List of Model objects containing
        updated fields. **(Required)**

        :Returns:
        - `Sequence[Model]`: List of updated records.

        """
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

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_id` (UUID | int): ID of record to delete. **(Required)**

        :Returns:
        - `Message | None`: Message indicating that record has been
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
    ) -> Message | None:
        """Delete multiple records by their IDs.

        :Args:
        - `db_session` (DBSession): SQLModel database session. **(Required)**
        - `record_ids` (list[UUID | int]): List of record IDs.
        **(Required)**

        :Returns:
        - `None`: Indicates that records have been deleted.

        """
        records: Sequence[Model] = await self.read_multiple_by_ids(
            db_session=db_session, record_ids=record_ids
        )

        for record in records:
            db_session.delete(instance=record)

        db_session.commit()

        return Message(message="Records deleted successfully")
