"""
User Pydantic Validators

Description:
- This module contains validators for user pydantic schemas.

"""

import re


def names_validator(name: str) -> str:
    """
    Name Validator

    Description:
    - This method is used to validate name data passed to API.

    Parameter:
    - **name** (STR): Name to be validated. **(Required)**

    Return:
    - **name** (STR): Validated name with capitalized.

    """

    if not name:
        return name

    if not re.search(r"^[a-zA-Z]*$", name):
        raise ValueError("Only alphabets are allowed")

    return name.capitalize()


def username_validator(username: str) -> str:
    """
    Username Validator

    Description:
    - This method is used to validate username data passed to API.

    Parameter:
    - **username** (STR): Username to be validated. **(Required)**

    Return:
    - **username** (STR): Validated username with lowered.

    """

    if not re.search(r"^[a-zA-Z0-9_.-]+$", username):
        raise ValueError(
            "Username can only contain alphabets, numbers, underscore, dot "
            "and hyphen"
        )

    return username.lower()


def lowercase_email(email: str) -> str:
    """
    Lowercase Email

    Description:
    - This method is used to lowercase email passed to API.

    Parameter:
    - **email** (STR): Email to be lowercased. **(Required)**

    Return:
    - **email** (STR): Lowercased email.

    """

    return email.lower()


def password_validator(password: str) -> str:
    """
    Password Validator

    Description:
    - This method is used to validate password data passed to API.

    Parameter:
    - **password** (STR): Password to be validated. **(Required)**

    Return:
    - **password** (STR): Validated password.

    """

    if not re.search(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^()_+-/])"
        r"[A-Za-z\d@$!%*?&#^()_+-/]{8,}$",
        password,
    ):
        raise ValueError(
            "Password should contain at least one uppercase, "
            "one lowercase and one special character"
        )

    return password
