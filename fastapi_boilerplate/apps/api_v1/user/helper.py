"""User Helper Module.

Description:
- This module contains all helper functions used by user package.

"""

import re

from passlib.context import CryptContext
from pydantic_extra_types.phone_numbers import PhoneNumber

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


def validate_contact(contact: PhoneNumber) -> str:
    """Validate Contact Number.

    :Description:
    - This method is used to validate contact number data.

    :Args:
    - `contact` (PhoneNumber): Contact number to validate. **(Required)**

    :Returns:
    - `contact` (str): Validated contact number.

    """
    return str(contact).replace("tel:", "")


def validate_username(username: str) -> str:
    """Username Validator.

    :Description:
    - This method is used to validate username data.

    :Args:
    - `username` (str): Username to validate. **(Required)**

    :Returns:
    - `username` (str): Validated username with lowered.

    """
    if not re.search(r"^[a-zA-Z0-9_.-]+$", username):
        raise ValueError(
            "Username can only contain alphabets, numbers, "
            "underscores, hyphens, and periods"
        )

    return username.lower()


def validate_email(email: str) -> str:
    """Validate Email.

    :Description:
    - This method is used to validate email.

    :Args:
    - `email` (str): Email to validate. **(Required)**

    :Returns:
    - `email` (str): Validated email with lowered.

    """
    return email.lower()


def validate_postal_code(postal_code: str) -> str:
    """Validate Postal Code.

    :Description:
    - This method is used to validate postal code data.

    :Args:
    - `postal_code` (str): Postal code to validate. **(Required)**

    :Returns:
    - `postal_code` (str): Validated postal code.

    """
    if not re.match(r"^\d{5}(-\d{4})?$", postal_code):
        raise ValueError(
            "Postal code must be in format '12345' or '12345-6789'"
        )

    return postal_code


def validate_password(password: str) -> str:
    """Validate Password.

    :Description:
    - This method is used to validate password data.

    :Args:
    - `password` (str): Password to validate. **(Required)**

    :Returns:
    - `password` (str): Validated password.

    """
    if not re.search(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^()_+-/])"
        r"[A-Za-z\d@$!%*?&#^()_+-/]{8,}$",
        password,
    ):
        raise ValueError(
            "Password must contain at least one lowercase letter, "
            "one uppercase letter, one number, and one special character"
        )

    return password
