"""
Core Helper Module

Description:
- This module contains all helper functions used by core module.
"""

from fastapi.routing import APIRoute


# Unique ID Generator for Routes
def custom_generate_unique_id(route: APIRoute) -> str:
    """
    Custom Generate Unique ID

    Description:
    - This function is used to return a custom unique id for routes.

    Parameter:
    - **route** (APIRoute): Route object. **(Required)**

    Return:
    - **id** (STR): Custom unique id.

    """

    return f"{route.tags[0]}-{route.name}"
