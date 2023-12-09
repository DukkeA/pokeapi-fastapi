import logging

from src.settings.base import settings


def setup_logging() -> None:
    """
    Configura la configuración de registro (logging) para la aplicación.

    Esta función configura el nivel de registro (logging level) para la aplicación
    según el valor especificado en la configuración de la aplicación (settings.LOG_LEVEL).
    """
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(levelname)s:     %(message)s',
    )
