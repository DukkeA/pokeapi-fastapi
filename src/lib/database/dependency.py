import logging
from typing import Generator

from sqlalchemy.orm import Session

from src.lib.database.base import session

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """
    Genera una instancia de sesión de base de datos.

    Returns:
        - Generator[Session, None, None]: Un generador que produce una instancia de sesión de
        base de datos.
    """
    logging.debug("Generating database session")
    db = session()
    try:
        yield db
    finally:
        logging.debug("Closing database session")
        db.close()
