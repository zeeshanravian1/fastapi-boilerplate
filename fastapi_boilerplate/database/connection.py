"""
Database Module

Description:
- This module is used to configure database connection and contains base
model for all tables.

"""

from datetime import datetime

from sqlalchemy import DateTime, Engine, MetaData, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)
from sqlalchemy.sql.functions import now

from fastapi_boilerplate.core.configuration import core_configuration

engine: Engine = create_engine(url=core_configuration.DATABASE_URL)
my_metadata: MetaData = MetaData()


class BaseTable(DeclarativeBase):
    """
    Base Table

    Description:
    - This is base model for all tables.

    """

    __abstract__ = True
    metadata: MetaData = my_metadata  # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=now()
    )

    @declared_attr.directive
    def __tablename__(self) -> str:
        """
        Generate table name automatically.

        """
        return (
            "".join(
                f"_{c.lower()}" if c.isupper() else c for c in self.__name__
            )
            .lstrip("_")
            .removesuffix("_table")
        )

    # Convert to dictionary
    def to_dict(self) -> dict:
        """
        Convert to dictionary.

        """

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
