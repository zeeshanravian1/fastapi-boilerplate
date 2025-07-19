"""User Repository.

Description:
- This module contains user repository implementation.

"""

from fastapi_boilerplate.apps.base.repository import BaseRepository

from .model import User, UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User Repository Class.

    :Description:
    - This class provides repository for user.

    """
