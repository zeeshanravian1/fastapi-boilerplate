"""User Helper Module.

Description:
- This module contains all helper functions used by user package.

"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Get Password Hash.

    :Description:
    - This function is used to get password hash.

    :Args:
    - `password` (str): Password. **(Required)**

    :Returns:
    - `hashed_password` (str): Hashed password.

    """
    return str(pwd_context.hash(secret=password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify Password.

    :Description:
    - This function is used to verify password.

    :Args:
    - `plain_password` (str): Plain password. **(Required)**
    - `hashed_password` (str): Hashed password. **(Required)**

    :Returns:
    - `is_verified` (bool): True if password is verified, False otherwise.

    """
    return bool(
        pwd_context.verify(secret=plain_password, hash=hashed_password)
    )
