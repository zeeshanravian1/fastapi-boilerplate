"""Session Module.

Description:
- This module is used to configure database session.

"""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from .connection import engine


class SessionManager:
    """Session manager for database.

    :Description:
    - This class is used to manage database sessions.

    """

    @staticmethod
    def get_session() -> Generator[Session]:
        """Get session.

        :Description:
        - This function is used to get session.

        :Args:
        - `None`

        :Yields:
        - `session` (Session): Database session.

        """
        with Session(bind=engine) as session:
            yield session


DBSession = Annotated[Session, Depends(dependency=SessionManager.get_session)]
