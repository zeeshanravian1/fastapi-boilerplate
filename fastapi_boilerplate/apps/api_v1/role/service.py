"""Role Service Module.

Description:
- This module contains role service.

"""

from fastapi_boilerplate.apps.base.service import BaseService

from .model import Role


class RoleService(BaseService[Role]):
    """Role Service Class.

    :Description:
    - This class provides service for role.

    """
