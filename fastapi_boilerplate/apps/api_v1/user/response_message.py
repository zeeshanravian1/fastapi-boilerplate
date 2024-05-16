"""
User Response Message Module

Description:
- This module is responsible for user response messages.

"""


class UserResponseMessage:
    """
    User Response Message Class

    Description:
    - This class is used to define user response messages.

    """

    USER_NOT_FOUND: str = "User not found"
    PASSWORD_CHANGED: str = "Password changed successfully"
    INCORRECT_PASSWORD: str = "Current password is incorrect"


user_response_message = UserResponseMessage()
