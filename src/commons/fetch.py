from typing import TypeVar, Union

from httpx import AsyncClient
from tenacity import retry, stop_after_attempt, wait_fixed

T = TypeVar("T")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def fetch_pokemon(
    client: AsyncClient, id: Union[int, str], response_class: T
) -> T:
    """
    Obtiene datos de un Pokémon desde una API con reintento.

    Esta función realiza una solicitud a una API para obtener datos de un Pokémon específico
    utilizando el ID proporcionado. La función utiliza un mecanismo de reintento en caso de
    que la solicitud falle. Los parámetros de reintento están configurados para realizar
    hasta 3 intentos, esperando 5 segundos entre cada intento.

    Args:
        - client (AsyncClient): Un cliente HTTP asincrónico para realizar la solicitud.
        - id (Union(int, str)): El ID o el nombre del Pokémon que se desea obtener.
        - response_class (Type[T]): El tipo de clase de respuesta en la que se convertirán los datos.

    Returns:
        - T: Un objeto de la clase `response_class` que contiene los datos del Pokémon obtenidos
          desde la API.

    Raises:
        - Exception: Si la solicitud falla después de todos los intentos de reintento.
    """
    response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    return response_class(**response.json())  # type: ignore


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def fetch_ability(
    client: AsyncClient, id: Union[int, str], response_class: T
) -> T:
    """
    Obtiene datos de una Habilidad desde una API con reintento.

    Esta función realiza una solicitud a una API para obtener datos de una habilidad específica
    utilizando el ID proporcionado. La función utiliza un mecanismo de reintento en caso de
    que la solicitud falle. Los parámetros de reintento están configurados para realizar
    hasta 3 intentos, esperando 5 segundos entre cada intento.

    Args:
        - client (AsyncClient): Un cliente HTTP asincrónico para realizar la solicitud.
        - id (Union(int, str)): El ID o el nombre de la habilidad que se desea obtener.
        - response_class (Type[T]): El tipo de clase de respuesta en la que se convertirán los datos.

    Returns:
        - T: Un objeto de la clase `response_class` que contiene los datos de la habilidad obtenidos
          desde la API.

    Raises:
        - Exception: Si la solicitud falla después de todos los intentos de reintento.
    """
    response = await client.get(f"https://pokeapi.co/api/v2/ability/{id}")
    return response_class(**response.json())  # type: ignore


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def fetch_type(
    client: AsyncClient, id: Union[int, str], response_class: T
) -> T:
    """
    Obtiene datos de un tipo desde una API con reintento.

    Esta función realiza una solicitud a una API para obtener datos de un tipo específico
    utilizando el ID proporcionado. La función utiliza un mecanismo de reintento en caso de
    que la solicitud falle. Los parámetros de reintento están configurados para realizar
    hasta 3 intentos, esperando 5 segundos entre cada intento.

    Args:
        - client (AsyncClient): Un cliente HTTP asincrónico para realizar la solicitud.
        - id (Union(int, str)): El ID o el nombre del tipo que se desea obtener.
        - response_class (Type[T]): El tipo de clase de respuesta en la que se convertirán los datos.

    Returns:
        - T: Un objeto de la clase `response_class` que contiene los datos del tipo obtenidos
          desde la API.

    Raises:
        - Exception: Si la solicitud falla después de todos los intentos de reintento.
    """
    response = await client.get(f"https://pokeapi.co/api/v2/type/{id}")
    return response_class(**response.json())  # type: ignore
