"""Connection Module.

Description:
- This module is used to configure database connection and contains base model
for all tables.

"""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Engine
from sqlalchemy.sql.functions import now
from sqlmodel import Column, DateTime, Field, MetaData, SQLModel, create_engine

from fastapi_boilerplate.core.config import settings

engine: Engine = create_engine(url=str(settings.SQLALCHEMY_DATABASE_URI))
my_metadata: MetaData = MetaData()


class Base(SQLModel):
    """Base Table.

    :Description:
    - This is base model for all tables.

    :Attributes:
    - `id` (UUID): Unique identifier for record.
    - `is_deleted` (bool): Flag to mark record as deleted.
    - `created_at` (datetime): Timestamp when record was created.
    - `updated_at` (datetime | None): Timestamp when record was last updated.
    - `deleted_at` (datetime | None): Timestamp when record was deleted.

    """

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    is_deleted: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=now())
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=True, onupdate=now()
        )
    )
    deleted_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=True, onupdate=now()
        )
    )

    class ModelConfig:  # pylint: disable=too-few-public-methods
        """Configuration for BaseTable."""

        str_strip_whitespace = True
