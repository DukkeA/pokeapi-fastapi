import logging
from datetime import datetime
from typing import List, Sequence

from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed

from src.lib.database import get_db
from src.settings import settings

from ..models import Pokemon
from ..schemas.pokemon_general.api import Pokemon as PokemonApi
from ..schemas.pokemon_general.api import PokemonResponse as PokemonResponseApi

logger = logging.getLogger(__name__)


class PokemonStartService:
    """
    Servicio de Inicio de Pokémon.

    Este servicio se encarga de inicializar y actualizar datos de Pokémon
    utilizando una API y una base de datos. Proporciona métodos para obtener
    datos de la API y la base de datos, y para actualizar la base de datos
    con los datos de la API.

    Args:
        - client (AsyncClient): Cliente asíncrono para realizar solicitudes a la API.
        - session (Session): Sesión de la base de datos para ejecutar consultas.

    Methods:
        - _get_from_db(self) -> Sequence[int]: Obtiene una secuencia de identificadores
          de Pokémon desde la base de datos.
        - _get_from_api(self, offset: int, limit: int) -> PokemonGeneralApiResponse:
          Obtiene datos generales de Pokémon desde una API.
        - _update_db(self, pokemons_from_api: List[PokemonGeneralApi],
          pokemons_in_db: Sequence[int]) -> None: Actualiza la base de datos con información
          de Pokémon obtenida de una API.
        - init_pokemons(self) -> None: Inicializa los datos de Pokémon obteniendo información
          de una API, comparándola con datos en la base de datos y actualizando la base de datos
          en consecuencia.
    """

    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    async def _get_from_db(self) -> Sequence[int]:
        """
        Obtiene una secuencia de identificadores de Pokémon desde la base de datos.

        Esta función ejecuta una consulta en la base de datos para obtener una secuencia
        de identificadores (IDs) de Pokémon que ya están almacenados en la base de datos.

        Returns:
            - Sequence[int]: Una secuencia de identificadores (IDs) de Pokémon presentes en
            la base de datos.
        """
        query = select(Pokemon.pokemon_id).select_from(Pokemon)
        return self.session.execute(query).scalars().all()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    async def _get_from_api(
        self, offset: int, limit: int
    ) -> PokemonResponseApi:
        """
        Obtiene datos generales de Pokémon desde una API con reintento automático.

        Esta función realiza una solicitud a una API para obtener información general
        sobre Pokémon, como nombres y URLs, a partir de un desplazamiento (offset) y un
        límite (limit) dados. Si la solicitud falla, se realizarán hasta 3 reintentos con
        un intervalo fijo de 5 segundos entre cada intento.

        Args:
            - offset (int): El desplazamiento en la lista de Pokémon a partir del cual se
            obtendrán los datos.
            - limit (int): El número máximo de Pokémon que se obtendrán en la solicitud.

        Returns:
            - PokemonGeneralApiResponse: Un objeto que contiene los datos generales de los
            Pokémon obtenidos de la API.
        """
        pokemons = await self.client.get(
            f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}"
        )
        return PokemonResponseApi(**pokemons.json())

    async def _update_db(
        self,
        pokemons_from_api: List[PokemonApi],
        pokemons_in_db: Sequence[int],
    ) -> None:
        """
        Actualiza la base de datos con información de Pokémon obtenida de una API.

        Este método toma una lista de datos de Pokémon de una API y una secuencia de IDs de Pokémon
        ya presentes en la base de datos. Compara los IDs y agrega cualquier nuevo Pokémon
        registros a la base de datos.

        Args:
            - pokemons_from_api (List[PokemonGeneralApi]): Una lista de datos de Pokémon obtenidos de la API.
            - pokemons_in_db (Sequence[int]): Una secuencia de IDs de Pokémon ya presentes en la base de datos.
        """
        for pokemon in pokemons_from_api:
            pokemon_id = int(pokemon.url.split("/")[-2])
            if pokemon_id in pokemons_in_db:
                continue
            self.session.add(
                Pokemon(
                    name=pokemon.name,
                    pokemon_id=pokemon_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )  # type: ignore
            )
            self.session.commit()

    async def init_pokemons(self) -> None:
        """
        Inicializa los datos de Pokémon obteniendo información de una API, comparándola con
        datos en la base de datos y actualizando la base de datos en consecuencia.

        Este método recupera un número especificado de Pokémon de una API y los compara con
        los datos de Pokémon en la base de datos. Luego actualiza la base de datos con
        la última información de la API.
        """
        numer_of_pokemons = settings.TOTAL_NUMBER_OF_POKEMONS
        pokemons = await self._get_from_api(offset=0, limit=numer_of_pokemons)
        pokemons_in_db = await self._get_from_db()
        await self._update_db(
            pokemons_from_api=pokemons.results, pokemons_in_db=pokemons_in_db
        )


async def init_pokemons(app: FastAPI):
    """
    Inicializa datos de Pokémon en la aplicación.

    Esta función se encarga de inicializar datos de Pokémon en la aplicación,
    utilizando un cliente asíncrono y una sesión de base de datos proporcionados
    como argumentos. Llama al método `init_pokemons` del servicio `PokemonStartService`
    para realizar la inicialización.

    Args:
        - app (FastAPI): La instancia de la aplicación FastAPI.
    """
    logging.info("Initializing pokemons started")
    session: Session = next(get_db())
    client: AsyncClient = app.requests  # type: ignore
    service = PokemonStartService(client=client, session=session)  # type: ignore
    logging.info("Initializing pokemons finished")
    await service.init_pokemons()
