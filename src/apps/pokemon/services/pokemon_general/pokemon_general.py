from typing import List, Optional

from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.settings import settings

from ...models.pokemon import Pokemon
from ...schemas.pokemon_general.base import Pokemon as PokemonBase
from ...schemas.pokemon_general.base import (
    PokemonResponse as PokemonResponseBase,
)


class PokemonGeneralService:
    """
    Servicio de obtencion de Pokémon reducido.

    Este servicio se encarga de obtener datos generales de Pokémon a partir de una URL
    especificada, utilizando una combinación de datos de la base de datos y la URL
    proporcionada. Proporciona métodos para obtener datos de la base de datos y formatear
    las URL de las páginas siguientes y anteriores.

    Args:
        - client (AsyncClient): Cliente asíncrono para realizar solicitudes a la API.
        - session (Session): Sesión de la base de datos para ejecutar consultas.

    Methods:
        - get_response(self) -> PokemonResponseBase: Obtiene una respuesta de
        datos generales de Pokémon.
        - _get_from_db(self, offset: int, limit: int, url: str) -> List[PokemonBase]:
        Obtiene datos generales de Pokémon desde la base de datos.
        - _get_formated_next_url(self, url: str, offset: int, limit: int) -> Optional[str]:
        Obtiene la URL formateada para la página siguiente de datos de Pokémon.
        - _get_formated_previous_url(self, url: str, offset: int, limit: int) -> Optional[str]:
        Obtiene la URL formateada para la página anterior de datos de Pokémon.
    """

    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    async def get_response(
        self, limit: int, offset: int, url: str
    ) -> PokemonResponseBase:
        """
        Obtiene una respuesta de datos generales de Pokémon.

        Esta función obtiene una respuesta de datos generales de Pokémon a partir de una URL
        especificada, utilizando una combinación de datos de la base de datos y la URL proporcionada.
        La respuesta incluye información sobre el número total de Pokémon, las URL siguientes y
        anteriores, y la lista de Pokémon en la página actual.

        Args:
            - limit (int): El número máximo de Pokémon a obtener.
            - offset (int): El desplazamiento en la lista de Pokémon a partir del cual se obtendrán los datos.
            - url (str): La URL desde la cual se obtendrán los datos generales de Pokémon.

        Returns:
            - PokemonResponseBase: Un objeto que contiene una respuesta de datos generales de Pokémon
            con el número total de Pokémon, las URL siguientes y anteriores, y la lista de Pokémon en
            la página actual.
        """
        pokemons = self._get_from_db(offset=offset, limit=limit, url=url)
        next_url = self._get_formated_next_url(
            url=url, offset=offset, limit=limit
        )
        previous_url = self._get_formated_previous_url(
            url=url, offset=offset, limit=limit
        )
        return PokemonResponseBase(
            count=settings.TOTAL_NUMBER_OF_POKEMONS,
            next=next_url,
            previous=previous_url,
            results=pokemons,
        )

    def _get_from_db(
        self, offset: int, limit: int, url: str
    ) -> List[PokemonBase]:
        """
        Obtiene datos generales de Pokémon desde la base de datos.

        Esta función realiza una consulta a la base de datos para obtener datos generales de
        Pokémon a partir de un desplazamiento (offset) y un límite (limit) especificados,
        y los formatea en una lista de objetos `PokemonBase`.

        Args:
            - offset (int): El desplazamiento en la lista de Pokémon a partir del cual se
            obtendrán los datos.
            - limit (int): El número máximo de Pokémon a obtener.
            - url (str): La URL base que se utilizará para construir las URL de los Pokémon.

        Returns:
            - List[PokemonBase]: Una lista de objetos `PokemonBase` que contienen datos
            generales de los Pokémon obtenidos desde la base de datos.
        """
        response = (
            self.session.query(Pokemon)
            .filter(Pokemon.pokemon_id.in_(range(offset, offset + limit)))
            .all()
        )
        base_url = url.split("?")[0]
        pokemons = [
            PokemonBase(
                id=pokemon.pokemon_id,
                name=pokemon.name,
                url=f"{base_url}/{pokemon.pokemon_id}",
            )
            for pokemon in response
        ]
        return pokemons

    def _get_formated_next_url(
        self, url: str, offset: int, limit: int
    ) -> Optional[str]:
        """
        Obtiene la URL formateada para la página siguiente de datos de Pokémon.

        Esta función recibe una URL base y calcula la URL de la página siguiente de datos de Pokémon
        basándose en el desplazamiento (offset) y el límite (limit) especificados. Si la página siguiente
        no existe (es decir, si se alcanza el límite total de Pokémon), la función devuelve `None`.

        Args:
            - url (str): La URL base a partir de la cual se generará la URL de la página siguiente.
            - offset (int): El desplazamiento actual en la lista de Pokémon.
            - limit (int): El número máximo de Pokémon por página.

        Returns:
            - Optional[str]: La URL formateada de la página siguiente de datos de Pokémon o `None` si
            no hay una página siguiente.
        """
        if offset + limit >= settings.TOTAL_NUMBER_OF_POKEMONS:
            return None
        base_url = url.split("?")[0]
        url = f"{base_url}?offset={offset + limit}&limit={limit}"
        return url

    def _get_formated_previous_url(
        self, url: str, offset: int, limit: int
    ) -> Optional[str]:
        """
        Obtiene la URL formateada para la página anterior de datos de Pokémon.

        Esta función recibe una URL base y calcula la URL de la página anterior de datos de Pokémon
        basándose en el desplazamiento (offset) y el límite (limit) especificados. Si la página anterior
        no existe (es decir, si ya estamos en la primera página), la función devuelve `None`.

        Args:
            - url (str): La URL base a partir de la cual se generará la URL de la página anterior.
            - offset (int): El desplazamiento actual en la lista de Pokémon.
            - limit (int): El número máximo de Pokémon por página.

        Returns:
            - Optional[str]: La URL formateada de la página anterior de datos de Pokémon o `None` si
            no hay una página anterior.
        """
        if offset == 0:
            return None
        base_url = url.split("?")[0]
        url = f"{base_url}?offset={offset - limit}&limit={limit}"
        return url


async def get_general_pokemons(
    limit: int, offset: int, url: str, client: AsyncClient, session: Session
) -> PokemonResponseBase:
    """
    Obtiene datos generales de Pokémon a partir de una URL especificada.

    Esta función utiliza un cliente asíncrono y una sesión de base de datos para obtener
    datos generales de Pokémon a partir de una URL especificada. Utiliza el servicio
    `PokemonGeneralService` para realizar la solicitud y procesar la respuesta.

    Args:
        - limit (int): El número máximo de Pokémon a obtener.
        - offset (int): El desplazamiento en la lista de Pokémon a partir del cual se obtendrán los datos.
        - url (str): La URL desde la cual se obtendrán los datos generales de Pokémon.
        - client (AsyncClient): Cliente asíncrono para realizar la solicitud HTTP.
        - session (Session): Sesión de base de datos para ejecutar consultas.

    Returns:
        - PokemonResponseBase: Un objeto que contiene los datos generales de los Pokémon obtenidos.
    """
    service = PokemonGeneralService(client=client, session=session)
    response = await service.get_response(limit=limit, offset=offset, url=url)
    return response
