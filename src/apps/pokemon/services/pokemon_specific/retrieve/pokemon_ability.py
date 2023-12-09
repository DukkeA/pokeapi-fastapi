from datetime import datetime
from typing import Optional, Sequence

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.commons.fetch import fetch_pokemon

from ....models import Ability, Pokemon, PokemonAbility
from ....schemas.pokemon_detailed.api.pokemon import (
    Pokemon as PokemonResponseApi,
)
from ....schemas.pokemon_detailed.base.pokemon import (
    PokemonAbility as PokemonAbilityBase,
)


class PokemonAbilityService:
    """
    Clase para gestionar las habilidades de Pokémon en la base de datos y la API.

    Args:
        - client (AsyncClient): El cliente HTTP asincrónico utilizado para realizar
        solicitudes.
        - session (Session): La sesión de base de datos SQLAlchemy utilizada para
        operaciones de base de datos.

    Methods:
        - async _get_ability_from_db(id: int) -> Optional[Ability]: Obtiene una
        habilidad de Pokémon desde la base de datos.
        - async _save_ability(name: str, internal_id: int) -> Ability: Guarda una
        nueva habilidad de Pokémon en la base de datos.
        - async update_abilities(pokemon: Pokemon) -> Sequence[PokemonAbilityBase]:
        Actualiza las habilidades de un Pokémon en la base de datos y devuelve una
        secuencia de objetos PokemonAbilityBase que representan las habilidades
        actualizadas.
    """

    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    async def _get_ability_from_db(self, id: int) -> Optional[Ability]:
        """
        Obtiene una habilidad de Pokémon desde la base de datos.

        Args:
            - id (int): El ID interno de la habilidad de Pokémon.

        Returns:
            - Optional[Ability]: Un objeto Ability que representa la habilidad
            encontrada en la base de datos o None si no se encuentra.
        """
        query = select(Ability).filter(Ability.internal_id == id)
        result = self.session.execute(query).scalars().first()
        return result

    async def _save_ability(self, name: str, internal_id: int) -> Ability:
        """
        Guarda una nueva habilidad de Pokémon en la base de datos.

        Args:
            - name (str): El nombre de la habilidad de Pokémon.
            - internal_id (int): El ID interno de la habilidad de Pokémon.

        Returns:
            - Ability: Un objeto Ability que representa la habilidad guardada en
            la base de datos.
        """
        ability = Ability(
            name=name,
            internal_id=internal_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )  # type: ignore
        self.session.add(ability)
        self.session.flush()
        return ability

    async def update_abilities(
        self, pokemon: Pokemon
    ) -> Sequence[PokemonAbilityBase]:
        """
        Actualiza las habilidades de un Pokémon en la base de datos y devuelve una
        secuencia de objetos PokemonAbilityBase.

        Este método obtiene las habilidades de un Pokémon desde la API y las almacena
        en la base de datos si no existen previamente. Luego, recupera las habilidades
        actualizadas desde la base de datos y las devuelve como una secuencia
        de objetos PokemonAbilityBase.

        Args:
            - pokemon (Pokemon): El Pokémon para el cual se actualizarán las habilidades.

        Returns:
            - Sequence[PokemonAbilityBase]: Una secuencia de objetos PokemonAbilityBase
            que representan las habilidades actualizadas.
        """
        pokemon_from_api = await fetch_pokemon(
            client=self.client,
            id=pokemon.pokemon_id,
            response_class=PokemonResponseApi,
        )
        if not pokemon_from_api:
            return []
        abilities_to_save: Sequence[PokemonAbility] = []
        for ability_from_api in pokemon_from_api.abilities:
            ability_id = int(ability_from_api.ability.url.split("/")[-2])  # type: ignore
            ability_from_db = await self._get_ability_from_db(id=ability_id)
            if not ability_from_db:
                ability_from_db = await self._save_ability(
                    name=ability_from_api.ability.name, internal_id=ability_id
                )
            abilities_to_save.append(
                PokemonAbility(
                    ability_id=ability_from_db.id,
                    pokemon_id=pokemon.id,
                )  # type: ignore
            )
        self.session.add_all(abilities_to_save)
        self.session.flush()
        return [
            PokemonAbilityBase(
                id=ability.ability.internal_id, name=ability.ability.name
            )
            for ability in abilities_to_save
        ]
