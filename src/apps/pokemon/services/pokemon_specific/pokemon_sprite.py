from datetime import datetime
from typing import Sequence

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.commons.fetch import fetch_pokemon

from ...models import Pokemon, Sprite
from ...models.sprite import SpriteType
from ...schemas.pokemon_detailed.api import Pokemon as PokemonResponseApi
from ...schemas.pokemon_detailed.base import PokemonSprite as PokemonSpriteBase


class PokemonSpriteService:
    """
    Servicio para manejar y actualizar los sprites de los Pokémon en la base de
    datos.

    Este servicio proporciona métodos para obtener y actualizar los sprites de
    los Pokémon en la base de datos. Utiliza un cliente HTTP asíncrono y una sesión
    de base de datos para realizar estas operaciones.

    Args:
        - client (AsyncClient): Cliente HTTP asíncrono para realizar solicitudes
        a la API.
        - session (Session): Sesión de base de datos para interactuar con la base
        de datos.

    Métodos:
        - _get_sprite_from_db(self, id: int, sprite_type: SpriteType) -> Sequence[Sprite]:
        Obtiene un sprite de la base de datos según el ID del Pokémon y el tipo
        de sprite.

        - _save_sprite(self, pokemon_id: int, sprite_type: SpriteType, url: str) -> Sprite:
        Guarda un nuevo sprite en la base de datos.

        - _get_sprite_url(self, api_response: PokemonResponseApi, sprite_type: str) -> str:
        Obtiene la URL del sprite a partir de la respuesta de la API y el tipo de sprite.

        - update_sprites(self, pokemon: Pokemon) -> Sequence[PokemonSpriteBase]:
        Actualiza los sprites de un Pokémon en la base de datos.

    """

    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    async def _get_sprite_from_db(
        self, id: int, sprite_type: SpriteType
    ) -> Sequence[Sprite]:
        """
        Obtiene un sprite de la base de datos según el ID del Pokémon y el tipo
        de sprite.

        Args:
            - id (int): El ID del Pokémon al que pertenece el sprite.
            - sprite_type (SpriteType): El tipo de sprite a obtener.

        Returns:
            - Sequence[Sprite]: Una secuencia de objetos `Sprite` que representan
            el sprite encontrado en la base de datos o una secuencia vacía si no
            se encuentra.
        """
        query = select(Sprite).filter(
            Sprite.pokemon_id == id, Sprite.sprite_type == sprite_type
        )
        result = self.session.execute(query).scalars().first()
        return result

    async def _save_sprite(
        self, pokemon_id: int, sprite_type: SpriteType, url: str
    ) -> Sprite:
        """
        Guarda un nuevo sprite en la base de datos.

        Args:
            - pokemon_id (int): El ID del Pokémon al que pertenece el sprite.
            - sprite_type (SpriteType): El tipo de sprite a guardar.
            - url (str): La URL del sprite a guardar.

        Returns:
            - Sprite: El objeto `Sprite` que representa el sprite guardado en la
            base de datos.
        """
        sprite = Sprite(
            pokemon_id=pokemon_id,
            sprite_type=sprite_type,
            url=url,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )  # type: ignore
        self.session.add(sprite)
        self.session.flush()
        return sprite

    def _get_sprite_url(
        self, api_response: PokemonResponseApi, sprite_type: str
    ) -> str:
        """
        Obtiene la URL del sprite a partir de la respuesta de la API y el tipo de
        sprite.

        Args:
            - api_response (PokemonResponseApi): La respuesta de la API que contiene
            información
              sobre los sprites del Pokémon.
            - sprite_type (str): El tipo de sprite a obtener (p. ej., "default",
            "dream_world").

        Returns:
            - str: La URL del sprite correspondiente al tipo especificado.
        """
        if SpriteType.DREAM_WORLD.value == sprite_type:
            return api_response.sprites.other.dream_world.front_default
        elif SpriteType.HOME.value == sprite_type:
            return api_response.sprites.other.home.front_default
        elif SpriteType.OFFICIAL_ARTWORK.value == sprite_type:
            return api_response.sprites.other.official_artwork.front_default
        else:
            return api_response.sprites.front_default

    async def update_sprites(
        self, pokemon: Pokemon
    ) -> Sequence[PokemonSpriteBase]:
        """
        Actualiza los sprites de un Pokémon en la base de datos.

        Este método obtiene los sprites de un Pokémon a través de la API y los
        guarda en la base de datos, asegurándose de que se almacenen diferentes
        tipos de sprites, como el sprite predeterminado y otros específicos.

        Args:
            - pokemon (Pokemon): El Pokémon para el cual se actualizarán los sprites.

        Returns:
            - Sequence[PokemonSpriteBase]: Una secuencia de objetos `PokemonSpriteBase`
            que representan los sprites actualizados del Pokémon.
        """
        pokemon_from_api = await fetch_pokemon(
            client=self.client,
            id=pokemon.pokemon_id,
            response_class=PokemonResponseApi,
        )
        if not pokemon_from_api:
            return []
        sprites_to_save: Sequence[Sprite] = []
        sprite_type_list_from_api = [sprite_type for sprite_type in SpriteType]
        for sprite_type_from_api in sprite_type_list_from_api:
            sprite_from_db = await self._get_sprite_from_db(
                id=pokemon.id, sprite_type=sprite_type_from_api
            )
            if not sprite_from_db:
                sprite_from_db = await self._save_sprite(
                    pokemon_id=pokemon.id,
                    sprite_type=sprite_type_from_api,
                    url=self._get_sprite_url(
                        api_response=pokemon_from_api,  # type: ignore
                        sprite_type=sprite_type_from_api.value,
                    ),
                )
                sprites_to_save.append(sprite_from_db)
        return [
            PokemonSpriteBase(
                type=sprite.sprite_type.value,
                url=sprite.url,
            )
            for sprite in sprites_to_save
        ]
