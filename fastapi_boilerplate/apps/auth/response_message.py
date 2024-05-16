"""
Authentication Response Message Module

Description:
- This module is responsible for auth response messages.

"""


class AuthResponseMessage:
    """
    Auth Response Message Class

    Description:
    - This class is used to define auth response messages.

    """

    USER_NOT_FOUND: str = "User not found"
    INCORRECT_PASSWORD: str = "Incorrect password"
    USER_LOGGED_OUT: str = "User logged out successfully"
    USERNAME_ALREADY_EXISTS: str = "Username already exists"
    EMAIL_ALREADY_EXISTS: str = "Email already exists"
    INVALID_EMAIL: str = "Invalid email"


auth_response_message = AuthResponseMessage()
