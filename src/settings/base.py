from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Attributes:
        - APP_NAME (str): El nombre de la aplicación.
        - APP_VERSION (str): La versión de la aplicación.
        - APP_ENVIRONMENT (str): El entorno de la aplicación (por ejemplo, "dev" o "prod").
        - DEBUG (bool): Indica si el modo de depuración está habilitado.
        - LOG_LEVEL (str): El nivel de registro de la aplicación.

        - DB_USER (str): El nombre de usuario de la base de datos.
        - DB_PASSWORD (str): La contraseña de la base de datos.
        - DB_HOST (str): La dirección del servidor de la base de datos.
        - DB_PORT (int): El puerto de la base de datos.
        - DB_NAME (str): El nombre de la base de datos.

        - TOTAL_NUMBER_OF_POKEMONS (int): El número total de Pokémon en la aplicación.

    Properties:
        - DB_URL (str): La URL de conexión a la base de datos PostgreSQL generada
        a partir de los atributos de la base de datos.

    Config:
        - env_file (str): El nombre del archivo de entorno que se utilizará para
        cargar las variables de configuración.
    """

    APP_NAME: str = "pokeapi"
    APP_VERSION: str = "0.0.1"
    APP_ENVIRONMENT: str = "dev"
    DEBUG: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"] = "INFO"

    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"

    TOTAL_NUMBER_OF_POKEMONS: int = 1017

    @property
    def DB_URL(self) -> str:  # noqa
        return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}".format(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )

    model_config = {"env_file": ".env"}


settings: Settings = Settings()
