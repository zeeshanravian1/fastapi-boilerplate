"""Role Repository.

Description:
- This module contains role repository implementation.

"""

from fastapi_boilerplate.apps.base.repository import BaseRepository

from .model import Role, RoleCreate, RoleUpdate


class RoleRepository(BaseRepository[Role, RoleCreate, RoleUpdate]):
    """Role Repository Class.

    :Description:
    - This class provides repository for role.

    """
