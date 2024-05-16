"""
Base Configuration Module

Description:
- This module is responsible for base routes configuration.

"""

from datetime import datetime, timezone


class BaseConfiguration:
    """
    Base Settings Class

    Description:
    - This class is used to define base configurations.

    """

    ID: int = 1
    CREATED_AT: datetime = datetime.now(tz=timezone.utc)
    UPDATED_AT: datetime = datetime.now(tz=timezone.utc)

    TOTAL_RECORDS: int = 1
    TOTAL_PAGES: int = 1
    PAGE: int = 1
    LIMIT: int = 10


base_configuration = BaseConfiguration()
