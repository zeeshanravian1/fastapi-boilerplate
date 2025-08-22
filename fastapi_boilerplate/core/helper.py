"""Core Helper Module.

Description:
- This module contains all helper functions used by core package.

"""

from fastapi.routing import APIRoute


class CoreHelper:
    """Core Helper Class.

    :Description:
    - This class contains all helper methods used by core package.

    """

    @staticmethod
    def parse_cors(cors: list[str] | str) -> list[str] | str:
        """Parse Cors.

        :Description:
        - This method is used to parse cors values.

        :Args:
        - `cors` (list[str] | str): Cors value. **(Required)**

        :Returns:
        - `cors` (list[str] | str): Cors value.

        """
        if isinstance(cors, str) and not cors.startswith("["):
            return [i.strip() for i in cors.split(sep=",")]

        if isinstance(cors, list | str):
            return cors

        raise ValueError(cors)

    @staticmethod
    def custom_generate_unique_id(route: APIRoute) -> str:
        """Custom Generate Unique ID.

        :Description:
        - This function is used to return a custom unique id for routes.

        :Args:
        - `route` (APIRoute): Route object. **(Required)**

        :Returns:
        - `id` (str): Custom unique id.

        """
        return f"{route.tags[0]}-{route.name}"
