from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from src.lib.database.dependency import get_db

from ..schemas.pokemon_detailed.base.pokemon import (
    PokemonInput,
    Pokemon as PokemonResponseBase,
)
from ..services.pokemon_specific.retrieve import (
    get_specific_pokemon,
)


async def get_pokemon_detailed(
    id: str, request: Request, session: Session = Depends(get_db)
) -> Optional[PokemonResponseBase]:
    """
    Obtiene detalles específicos de un Pokémon.

    Esta función realiza una solicitud a una API para obtener detalles específicos
    de un Pokémon identificado por su ID. Utiliza el cliente HTTP proporcionado
    en la solicitud y la sesión de base de datos para recuperar los datos del
    Pokémon. Si el Pokémon no se encuentra o si la solicitud falla, la función
    devuelve `None`.

    Args:
        - id (str): El ID del Pokémon que se desea obtener.
        - request (Request): El objeto de solicitud FastAPI que contiene información
        sobre la aplicación.
        - session (Session, opcional): La sesión de base de datos a utilizar. Si
        no se proporciona, se obtendrá una sesión nueva utilizando la función
        `get_db()`.

    Returns:
        - Optional[PokemonResponseBase]: Un objeto que contiene detalles específicos
        del Pokémon obtenidos desde la API o `None` si el Pokémon no se encuentra
        o la solicitud falla.
    """
    client = request.app.requests
    response = await get_specific_pokemon(
        id=id, client=client, session=session
    )
    return response


async def update_pokemon_detailed(
    id: str,
    body: PokemonInput,
    request: Request,
    session: Session = Depends(get_db),
) -> PokemonResponseBase:
    ...
