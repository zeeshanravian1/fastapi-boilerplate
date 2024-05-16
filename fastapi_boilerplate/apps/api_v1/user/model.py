"""
User Model

Description:
- This file contains model for user table.

"""

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_boilerplate.database.connection import BaseTable

from ..role.model import RoleTable


class UserTable(BaseTable):
    """
    User Table

    Description:
    - This table is used to create user in database.

    """

    name: Mapped[str] = mapped_column(String(2_55))
    username: Mapped[str] = mapped_column(String(2_55), unique=True)
    email: Mapped[str] = mapped_column(String(2_55), unique=True)
    password: Mapped[str] = mapped_column(String(2_55))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Foreign Keys
    role_id: Mapped[int] = mapped_column(
        ForeignKey(RoleTable.id, ondelete="CASCADE")
    )

    # Relationships
    role: Mapped[RoleTable] = relationship(
        back_populates="users", lazy="subquery"
    )
