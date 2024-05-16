"""
Session Module

Description:
- This module is used to configure database session.

"""

from sqlalchemy.orm import Session, sessionmaker

from .connection import engine

SessionLocal = sessionmaker(autoflush=True, bind=engine, expire_on_commit=True)


def get_session() -> Session:
    """
    Get session

    Description:
    - This function is used to get session.

    Parameters:
    - **None**

    Returns:
    - **session** (AsyncSession): Session.

    """

    session: Session = SessionLocal()

    try:
        return session

    except Exception as err:
        session.rollback()
        raise err

    finally:
        session.close()
