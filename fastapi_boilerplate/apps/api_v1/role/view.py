"""
Role View Module

Description:
- This module is responsible for role views.

"""

from typing import Type

from fastapi_boilerplate.apps.base.view import BaseView

from .model import RoleTable
from .schema import RoleCreateSchema, RoleUpdateSchema


# Role class
class RoleView(
    BaseView[
        RoleTable,
        RoleCreateSchema,
        RoleUpdateSchema,
    ]
):
    """
    Role View Class

    Description:
    - This class is responsible for role views.

    """

    def __init__(
        self,
        model: Type[RoleTable],
    ) -> None:
        """
        Role View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (RoleTable): Role Database Model.

        """

        super().__init__(model=model)


role_view = RoleView(model=RoleTable)
