"""
Core Pydantic Schemas

Description:
- This module contains all core schemas used by API.

"""

from pydantic import Field

from ..apps.api_v1.role.configuration import role_configuration
from ..apps.api_v1.user.schema import UserReadSchema


class CurrentUserReadSchema(UserReadSchema):
    """
    Current User Read Schema

    Description:
    - This schema is used to validate current user data.

    """

    role_name: str = Field(examples=[role_configuration.ROLE_NAME])
