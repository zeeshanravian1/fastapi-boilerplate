"""
User Configuration Module

Description:
- This module is responsible for user configuration.

"""


class UserConfiguration:
    """
    User Settings Class

    Description:
    - This class is used to define user configurations.

    """

    NAME: str = "John Doe"
    USERNAME: str = "johndoe"
    EMAIL: str = "johndoe@email.com"
    PASSWORD: str = "12345@Aa"
    ROLE_ID: int = 1
    USER_COLUMN_USERNAME: str = "username"
    USER_COLUMN_EMAIL: str = "email"


user_configuration = UserConfiguration()
