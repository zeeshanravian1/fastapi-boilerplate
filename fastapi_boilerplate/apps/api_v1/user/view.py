"""
User View Module

Description:
- This module is responsible for user views.

"""

from typing import Type

from passlib.hash import pbkdf2_sha256
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.sql.dml import Update

from fastapi_boilerplate.apps.base.view import BaseView

from .model import UserTable
from .response_message import user_response_message
from .schema import PasswordChangeSchema, UserCreateSchema, UserUpdateSchema


# User class
class UserView(
    BaseView[
        UserTable,
        UserCreateSchema,
        UserUpdateSchema,
    ]
):
    """
    User View Class

    Description:
    - This class is responsible for user views.

    """

    def __init__(
        self,
        model: Type[UserTable],
    ) -> None:
        """
        User View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (UserTable): User Database Model.

        """

        super().__init__(model=model)

    async def create(
        self, db_session: Session, record: UserCreateSchema
    ) -> UserTable:
        """
        Create User

        Description:
        - This method is responsible for creating a user.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record** (UserCreateSchema): User create schema. **(Required)**

        Return:
        - **record** (UserTable): UserTable object.

        """

        record.password = pbkdf2_sha256.hash(record.password)

        return await super().create(db_session=db_session, record=record)

    async def password_change(
        self,
        db_session: Session,
        record_id: int,
        record: PasswordChangeSchema,
    ) -> dict[str, str]:
        """
        Change Password

        Description:
        - This method is responsible for changing user password.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (INT): Id of user. **(Required)**
        - **record** (PasswordChangeSchema): Password change schema.
        **(Required)**

        Return:
        - **detail** (STR): Password changed successfully.

        """

        result: UserTable | None = await super().read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not result:
            return {"detail": user_response_message.USER_NOT_FOUND}

        if not pbkdf2_sha256.verify(record.old_password, result.password):
            return {"detail": user_response_message.INCORRECT_PASSWORD}

        query: Update = (
            update(self.model)
            .where(self.model.id == record_id)
            .values(password=pbkdf2_sha256.hash(record.new_password))
        )
        db_session.execute(statement=query)
        db_session.commit()

        return {"detail": user_response_message.PASSWORD_CHANGED}


user_view = UserView(model=UserTable)
