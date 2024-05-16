"""
Authentication Configuration Module

Description:
- This module is responsible for auth configuration.

"""


class AuthConfiguration:
    """
    Authentication Settings Class

    Description:
    - This class is used to define auth configurations.

    """

    TOKEN_TYPE: str = "bearer"
    ROLE_NAME: str = "admin"


auth_configuration = AuthConfiguration()
