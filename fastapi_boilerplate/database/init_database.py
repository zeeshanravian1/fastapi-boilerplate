"""
Insert initial data in database.

Description:
- This module is responsible for inserting initial data in database.

"""

import logging
from typing import Any

from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.sql.selectable import Select

from fastapi_boilerplate.apps.api_v1.role.model import RoleTable
from fastapi_boilerplate.apps.api_v1.user.model import UserTable
from fastapi_boilerplate.core.configuration import core_configuration

from .session import get_session

db_create_logger: logging.Logger = logging.getLogger(__name__)


# Creat roles in database
def create_roles(session=get_session()) -> None:
    """
    Create Roles

    Description:
    - This function is used to create roles in database.

    Parameter:
    - **None**

    Return:
    - **None**

    """

    roles: list[RoleTable] = [
        RoleTable(
            role_name=core_configuration.SUPERUSER_ROLE,
            role_description=core_configuration.SUPERUSER_ROLE_DESCRIPTION,
        )
    ]

    try:
        session.add_all(roles)
        session.commit()

    except (IntegrityError, ProgrammingError) as err:
        db_create_logger.exception(msg=err)


# Create super admin in database
def create_super_admin(session=get_session()) -> None:
    """
    Create Super Admin

    Description:
    - This function is used to create super admin in database.

    Parameter:
    - **None**

    Return:
    - **None**

    """

    try:
        # Get role id of Super Admin
        query: Select = select(RoleTable).where(
            RoleTable.role_name == core_configuration.SUPERUSER_ROLE
        )
        result: Result[Any] = session.execute(statement=query)
        role: RoleTable | None = result.scalars().first()

        if not role:
            db_create_logger.error(
                msg="Super Admin role not found in database."
            )
            return None

        # Create super admin
        super_user = UserTable(
            name=core_configuration.SUPERUSER_NAME,
            username=core_configuration.SUPERUSER_USERNAME,
            email=core_configuration.SUPERUSER_EMAIL,
            password=pbkdf2_sha256.hash(core_configuration.SUPERUSER_PASSWORD),
            role_id=role.id,
        )

        session.add(instance=super_user)
        session.commit()

    except (IntegrityError, ProgrammingError) as err:
        db_create_logger.exception(msg=err)
        db_create_logger.exception(msg=err)
