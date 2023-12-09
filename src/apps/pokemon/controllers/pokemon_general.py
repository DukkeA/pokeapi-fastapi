from fastapi import Depends, Request
from sqlalchemy.orm import Session

from src.lib.database.dependency import get_db

from ..schemas.pokemon_general.base.pokemon import (
    PokemonResponse as PokemonResponseBase,
)
from ..services import get_general_pokemons


async def get_pokemon_general(
    request: Request,
    session: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
) -> PokemonResponseBase:
    """
    Obtiene una respuesta de datos generales de Pokémon.

    Esta función maneja una solicitud HTTP para obtener una respuesta de datos generales de Pokémon
    a partir de una URL especificada. Utiliza una combinación de datos de la base de datos y la URL
    proporcionada para generar la respuesta, que incluye información sobre el número total de Pokémon,
    las URL siguientes y anteriores, y la lista de Pokémon en la página actual.

    Args:
        - request (Request): Objeto de solicitud HTTP.
        - session (Session, opcional): Sesión de base de datos para ejecutar consultas. Se obtiene mediante
          la función `get_db` y es opcional.
        - limit (int, opcional): El número máximo de Pokémon a obtener. El valor predeterminado es 20.
        - offset (int, opcional): El desplazamiento en la lista de Pokémon a partir del cual se obtendrán
          los datos. El valor predeterminado es 0.

    Returns:
        - PokemonResponseBase: Un objeto que contiene una respuesta de datos generales de Pokémon
        con el número total de Pokémon, las URL siguientes y anteriores, y la lista de Pokémon en
        la página actual.
    """
    client = request.app.requests
    response = await get_general_pokemons(
        limit=limit,
        offset=offset,
        client=client,
        session=session,
        url=str(request.url),
    )
    return response
