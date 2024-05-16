"""
Base View Module

Description:
- This module is responsible for base views.

"""

from math import ceil
from typing import Generic, Tuple, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Result, delete, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.dml import Delete, Update
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.selectable import Select

from ...database.connection import BaseTable

Model = TypeVar("Model", bound=BaseTable)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseView(
    Generic[
        Model,
        CreateSchema,
        UpdateSchema,
    ]
):
    """
    Base View Class

    Description:
    - This class is responsible for base views.

    """

    def __init__(self, model: Type[Model]):
        """
        Base View Class Initialization

        Description:
        - This method is responsible for CRUD object with default methods to
        Create, Read, Update and Delete.

        Parameter:
        - **model** (Model): SqlAlchemy Model. **(Required)**

        """

        self.model: type[Model] = model

    async def create(self, db_session: Session, record: CreateSchema) -> Model:
        """
        Create method

        Description:
        - This method is responsible for creating a single record.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record** (CreateSchema): Create Schema. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        db_instance: Model = self.model(**record.model_dump())
        db_session.add(instance=db_instance)
        db_session.commit()
        db_session.refresh(instance=db_instance)

        return db_instance

    async def read_by_id(
        self, db_session: Session, record_id: int
    ) -> Model | None:
        """
        Read Method

        Description:
        - This method is responsible for reading a single record by ID.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (int): Record ID. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        return db_session.query(self.model).get(record_id)

    async def read_all(
        self,
        db_session: Session,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict:
        """
        Read All Method

        Description:
        - This method is responsible for reading all records.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **page** (int): Page number. **(Optional)**
        - **limit** (int): Limit number. **(Optional)**

        Return:
        - **records** (JSON): Pagination Read Schema.

        """

        count_query: Select[tuple[int]] = select(count(self.model.id))
        total_records: int | None = db_session.execute(
            statement=count_query
        ).scalar()

        query: Select[Tuple[Model]] = select(self.model).order_by(
            self.model.id
        )

        if page and limit:
            query = (
                select(self.model)
                .where(self.model.id > (page - 1) * limit)
                .order_by(self.model.id)
                .limit(limit)
            )

        result: Result[Tuple[Model]] = db_session.execute(statement=query)

        if not (page and limit):
            return {
                "total_records": total_records,
                "total_pages": 1,
                "page": 1,
                "limit": total_records,
                "records": result.scalars().all(),
            }

        return {
            "total_records": total_records,
            "total_pages": ceil(total_records / limit),  # type: ignore
            "page": page,
            "limit": limit,
            "records": result.scalars().all(),
        }

    async def update(
        self, db_session: Session, record_id: int, record: UpdateSchema
    ) -> Model | None:
        """
        Update Method

        Description:
        - This method is responsible for updating a single record.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (int): Record ID. **(Required)**
        - **record** (UpdateSchema): Update Schema. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        query: Update = (
            update(self.model)
            .where(self.model.id == record_id)
            .values(record.model_dump(exclude_unset=True))
        )
        db_session.execute(statement=query)
        db_session.commit()

        return await self.read_by_id(
            db_session=db_session, record_id=record_id
        )

    async def delete(
        self, db_session: Session, record_id: int
    ) -> Model | None:
        """
        Delete Method

        Description:
        - This method is responsible for deleting a single record.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (int): Record ID. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        result: Model | None = await self.read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not result:
            return None

        query: Delete = delete(self.model).where(self.model.id == record_id)
        db_session.execute(statement=query)
        db_session.commit()

        return result
