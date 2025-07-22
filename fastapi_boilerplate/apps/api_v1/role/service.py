"""Role Service.

Description:
- This module contains role service implementation.

"""

from fastapi_boilerplate.apps.base.service import BaseService

from .model import Role, RoleCreate, RoleUpdate
from .repository import RoleRepository


class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    """Role Service Class.

    :Description:
    - This class provides business logic for role operations.

    """

    def __init__(self) -> None:
        """Initialize RoleService with RoleRepository."""
        super().__init__(repository=RoleRepository(model=Role))
        self.role_repository = RoleRepository(model=Role)
