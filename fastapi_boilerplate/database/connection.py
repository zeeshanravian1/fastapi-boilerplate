"""Connection Module.

Description:
- This module is used to configure database connection and contains base model
for all tables.

"""

from datetime import datetime
from uuid import UUID, uuid4  # noqa: F401

from sqlalchemy import Engine
from sqlalchemy.sql.functions import now
from sqlmodel import DateTime, Field, SQLModel, create_engine

from fastapi_boilerplate.core.config import settings

engine: Engine = create_engine(url=str(settings.SQLALCHEMY_DATABASE_URI))


class Base(SQLModel):
    """Base Table.

    :Description:
    - This is base model for all tables.

    :Attributes:
    - `id` (UUID | int): Unique identifier for record.
    - `created_at` (datetime): Timestamp when record was created.
    - `updated_at` (datetime | None): Timestamp when record was last updated.

    """

    id: int = Field(primary_key=True)
    # id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        sa_column_kwargs={"server_default": now()},
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        nullable=True,
        sa_column_kwargs={"onupdate": now()},
    )
