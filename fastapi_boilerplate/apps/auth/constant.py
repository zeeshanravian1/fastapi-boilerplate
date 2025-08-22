"""Authentication Constants.

Description:
- This module contains authentication constants.

"""

from enum import Enum

TOKEN_TYPE: str = "Bearer"


class TokenType(str, Enum):
    """Token Type Enum.

    :Description:
    - This enum is used to define token type.

    """

    ACCESS_TOKEN = "access_token"  # nosec B105
    REFRESH_TOKEN = "refresh_token"  # nosec B105
