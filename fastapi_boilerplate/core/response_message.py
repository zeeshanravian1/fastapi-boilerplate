"""
Core Response Message Module

Description:
- This module is responsible for core response messages.

"""


class CoreResponseMessage:
    """
    Core Response Message Class

    Description:
    - This class is used to define core response messages.

    """

    INVALID_TOKEN: str = "Invalid token"
    TOKEN_EXPIRED: str = "Token expired"
    INTEGRITY_ERROR: str = "Integrity error"
    INVALID_RESPONSE_BODY: str = "Invalid response body"
    INTERNAL_SERVER_ERROR: str = "Internal server error"


core_response_message = CoreResponseMessage()
