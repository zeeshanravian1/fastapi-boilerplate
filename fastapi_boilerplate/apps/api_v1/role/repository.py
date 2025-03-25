"""Role Repository Module.

Description:
- This module contains role repository.

"""

from fastapi_boilerplate.apps.base.repository import BaseRepository

from .model import Role


class RoleRepository(BaseRepository[Role]):
    """Role Repository Class.

    :Description:
    - This class provides repository for role.

    """
