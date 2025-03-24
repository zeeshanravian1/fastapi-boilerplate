"""Session Module.

Description:
- This module is used to configure database session.

"""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from .connection import engine


def get_session() -> Generator[Session]:
    """Get session.

    :Description:
    - This function is used to get session.

    :Returns:
    - `session` (Session): Database session.

    """
    with Session(bind=engine) as session:
        yield session


DBSession = Annotated[Session, Depends(dependency=get_session)]
