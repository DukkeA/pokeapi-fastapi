from datetime import datetime
from typing import Optional, Sequence

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.commons.fetch import fetch_pokemon

from ...models import Ability, Pokemon, PokemonType, Type
from ...schemas.pokemon_detailed.api import Pokemon as PokemonResponseApi
from ...schemas.pokemon_detailed.base import PokemonType as PokemonTypeBase


class PokemonTypeService:
    """
    Clase para gestionar los tipos de Pokémon en la base de datos y la API.

    Args:
        - client (AsyncClient): El cliente HTTP asincrónico utilizado para realizar
        solicitudes.
        - session (Session): La sesión de base de datos SQLAlchemy utilizada para
        operaciones de base de datos.

    Methods:
        - async _get_type_from_db(id: int) -> Optional[Type]: Obtiene un tipo de
        Pokémon desde la base de datos.
        - async _save_type(name: str, internal_id: int) -> Ability: Guarda un nuevo
        tipo de Pokémon en la base de datos.
        - async update_types(pokemon: Pokemon) -> Sequence[PokemonTypeBase]: Actualiza
        los tipos de un Pokémon en la base de datos y devuelve una secuencia de
        objetos PokemonTypeBase que representan los tipos actualizados.
    """

    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    async def _get_type_from_db(self, id: int) -> Optional[Type]:
        """
        Obtiene un tipo de Pokémon desde la base de datos.

        Args:
            - id (int): El ID interno del tipo de Pokémon que se desea obtener.

        Returns:
            - Optional[Type]: Un objeto que representa el tipo de Pokémon si se
            encuentra en la base de datos, o `None` si no se encuentra.
        """
        query = select(Type).filter(Type.internal_id == id)
        result = self.session.execute(query).scalars().first()
        return result

    async def _save_type(self, name: str, internal_id: int) -> Ability:
        """
        Guarda un nuevo tipo de Pokémon en la base de datos.

        Args:
            - name (str): El nombre del nuevo tipo de Pokémon.
            - internal_id (int): El ID interno del nuevo tipo de Pokémon.

        Returns:
            - Ability: El tipo de Pokémon creado y guardado en la base de datos.
        """
        pokemon_type = Type(
            name=name,
            internal_id=internal_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )  # type: ignore
        self.session.add(pokemon_type)
        self.session.flush()
        return pokemon_type

    async def update_types(
        self, pokemon: Pokemon
    ) -> Sequence[PokemonTypeBase]:
        """
        Actualiza los tipos de un Pokémon en la base de datos.

        Esta función obtiene los tipos de un Pokémon desde la API y los actualiza
        en la base de datos si no existen previamente. Luego, devuelve los tipos
        actualizados en forma de objetos PokemonTypeBase.

        Args:
            - pokemon (Pokemon): El Pokémon para el cual se actualizarán los tipos.

        Returns:
            - Sequence[PokemonTypeBase]: Una secuencia de objetos PokemonTypeBase
            que representan los tipos actualizados del Pokémon.
        """
        pokemon_from_api = await fetch_pokemon(
            client=self.client,
            id=pokemon.pokemon_id,
            response_class=PokemonResponseApi,
        )
        if not pokemon_from_api:
            return []
        types_to_save: Sequence[PokemonType] = []
        for type_from_api in pokemon_from_api.types:
            type_id = int(type_from_api.type.url.split("/")[-2])  # type: ignore
            type_from_db = await self._get_type_from_db(id=type_id)
            if not type_from_db:
                type_from_db = await self._save_type(
                    name=type_from_api.type.name, internal_id=type_id
                )
            types_to_save.append(
                PokemonType(
                    type_id=type_from_db.id,
                    pokemon_id=pokemon.id,
                )  # type: ignore
            )
        self.session.add_all(types_to_save)
        self.session.flush()
        return [
            PokemonTypeBase(
                id=pokemon_type.type.internal_id, name=pokemon_type.type.name
            )
            for pokemon_type in types_to_save
        ]
