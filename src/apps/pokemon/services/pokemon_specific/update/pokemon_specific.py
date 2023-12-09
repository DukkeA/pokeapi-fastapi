from httpx import AsyncClient
from sqlalchemy.orm import Session
from ....schemas.pokemon_detailed.base.pokemon import (
    PokemonInput,
    PokemonSpriteInput,
    Pokemon as PokemonResponse,
    PokemonAbility as PokemonAbilitySchema,
    PokemonType as PokemonTypeSchema,
    PokemonSprite as PokemonSpriteSchema,
)
from ....schemas.pokemon_detailed.api.ability import (
    Ability as AbilityApiResponse,
)
from ....schemas.pokemon_detailed.api.type import (
    Type as TypeApiResponse,
)
from ....models import (
    Pokemon,
    Ability,
    PokemonAbility,
    Type,
    PokemonType,
    Sprite,
)
from sqlalchemy import select
from typing import List, Union, Optional
from src.commons.fetch import fetch_ability, fetch_type
from datetime import datetime


class PokemonSpecificUpdateService:
    """
    Servicio para actualizar detalles específicos de Pokémon en la base de datos.

    Args:
        - client (AsyncClient): Cliente asincrónico utilizado para realizar
        solicitudes externas.
        - session (Session): Sesión de base de datos utilizada para interactuar
        con la base de datos.

    Métodos:
        - _get_pokemon_from_db(id: str) -> Pokemon:
        Obtiene un Pokémon de la base de datos por su ID o nombre.

        - _get_ability_from_db(id: str) -> Optional[Ability]:
        Obtiene una habilidad de la base de datos por su ID o nombre.

        - _get_type_from_db(id: str) -> Optional[Type]:
        Obtiene un tipo de la base de datos por su ID o nombre.

        - _update_abilities(abilities: Union[List[int], List[str]], pokemon_id: int) -> List[PokemonAbilitySchema]:
        Actualiza las habilidades de un Pokémon en la base de datos.

        - _update_types(types: Union[List[int], List[str]], pokemon_id: int) -> List[PokemonTypeSchema]:
        Actualiza los tipos de un Pokémon en la base de datos.

        - _update_sprites(sprites: List[PokemonSpriteInput], pokemon_id: int) -> List[PokemonSpriteSchema]:
        Actualiza los sprites de un Pokémon en la base de datos.

        - get_response(id: str, body: PokemonInput) -> PokemonResponse:
        Obtiene y actualiza la respuesta detallada de un Pokémon.
    """

    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    def _get_pokemon_from_db(self, id: str) -> Pokemon:
        """
        Obtiene un Pokémon de la base de datos por su ID o nombre.

        Este método toma como entrada un ID o nombre de Pokémon (id) y busca en
        la base de datos un registro de Pokémon que coincida con el ID o nombre
        proporcionado. Si se encuentra un registro de Pokémon, se devuelve; de
        lo contrario, se genera una excepción 'Pokemon not found'.

        Args:
            - id (str): El ID o nombre del Pokémon a buscar en la base de datos.

        Returns:
            - Pokemon: Un registro de Pokémon encontrado en la base de datos.

        Raises:
            - Exception: Si no se encuentra ningún Pokémon que coincida con el
            ID o nombre proporcionado.
        """
        query = select(Pokemon)
        if id.isnumeric():
            query = query.filter(Pokemon.pokemon_id == id)
        else:
            query = query.filter(Pokemon.name == id)
        result = self.session.execute(query).scalars().first()
        if not result:
            raise Exception('Pokemon no encontrado.')
        return result

    def _get_ability_from_db(self, id: str) -> Optional[Ability]:
        """
        Obtiene una habilidad de la base de datos por su ID o nombre.

        Este método toma como entrada un ID o nombre de habilidad (id) y busca en
        la base de datos un registro de habilidad que coincida con el ID o nombre
        proporcionado. Si se encuentra un registro de habilidad, se devuelve; de
        lo contrario, se devuelve None.

        Args:
            - id (str): El ID o nombre de la habilidad a buscar en la base de datos.

        Returns:
            - Optional[Ability]: Un registro de habilidad encontrado en la base
            de datos o None si no se encuentra coincidencia.
        """
        if id.isnumeric():
            query = select(Ability).filter(Ability.internal_id == id)
        else:
            query = select(Ability).filter(Ability.name == id)
        result = self.session.execute(query).scalars().first()
        return result

    def _get_type_from_db(self, id: str) -> Optional[Type]:
        """
        Obtiene un tipo de la base de datos por su ID o nombre.

        Este método toma como entrada un ID o nombre de tipo (id) y busca en la base
        de datos un registro de tipo que coincida con el ID o nombre proporcionado.
        Si se encuentra un registro de tipo, se devuelve; de lo contrario, se devuelve
        None.

        Args:
            - id (str): El ID o nombre del tipo a buscar en la base de datos.

        Returns:
            - Optional[Type]: Un registro de tipo encontrado en la base de datos o
            None si no se encuentra coincidencia.
        """
        if id.isnumeric():
            query = select(Type).filter(Type.internal_id == id)
        else:
            query = select(Type).filter(Type.name == id)
        result = self.session.execute(query).scalars().first()
        return result

    async def _update_abilities(
        self, abilities: Union[List[int], List[str]], pokemon_id: int
    ) -> List[PokemonAbilitySchema]:
        """
        Actualiza las habilidades de un Pokémon en la base de datos.

        Este método realiza las siguientes acciones:
        - Crea instancias de registros de habilidades (Ability) a partir de los IDs
        o nombres de habilidades proporcionados.
        - Verifica si las habilidades ya existen en la base de datos; si no, realiza
        una solicitud externa para obtener la
          información de la habilidad y crea un nuevo registro de habilidad.
        - Elimina los registros de habilidades existentes en la base de datos que
        pertenecen al Pokémon especificado.
        - Agrega los nuevos registros de habilidades a la base de datos.
        - Devuelve una lista de esquemas de habilidades actualizadas del Pokémon.

        Args:
            - abilities (Union[List[int], List[str]]): Una lista de IDs o nombres de
            habilidades proporcionados en la solicitud.
            - pokemon_id (int): El ID del Pokémon al que pertenecen las habilidades.

        Returns:
            - List[PokemonAbilitySchema]: Una lista de esquemas de habilidades actualizadas
            del Pokémon.
        """
        abilities_saved: List[Ability] = []
        for ability in abilities:
            ability_from_db = self._get_ability_from_db(id=str(ability))
            if not ability_from_db:
                try:
                    ability_from_api = await fetch_ability(
                        client=self.client,
                        id=ability,
                        response_class=AbilityApiResponse,
                    )
                except Exception as e:
                    raise Exception(
                        f'Habilidad {ability} no encontrada.'
                    ) from e
                if not ability_from_api:
                    raise Exception(f'Habilidad {ability} no encontrada.')
                ability_from_db = Ability(
                    name=ability_from_api.name,
                    internal_id=ability_from_api.id,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )  # type: ignore
                self.session.add(ability_from_db)
                self.session.flush()
            abilities_saved.append(
                PokemonAbility(
                    pokemon_id=pokemon_id, ability_id=ability_from_db.id
                )  # type: ignore
            )
        self.session.query(PokemonAbility).filter(
            PokemonAbility.pokemon_id == pokemon_id
        ).delete()
        self.session.add_all(abilities_saved)
        self.session.flush()
        return [
            PokemonAbilitySchema(
                id=ability.ability.internal_id,  # type: ignore
                name=ability.ability.name,  # type: ignore
            )
            for ability in abilities_saved
        ]

    async def _update_types(
        self, types: Union[List[int], List[str]], pokemon_id: int
    ) -> List[PokemonTypeSchema]:
        """
        Actualiza los tipos de un Pokémon en la base de datos.

        Este método realiza las siguientes acciones:
        - Crea instancias de registros de tipos (Type) a partir de los IDs o nombres
        de tipos proporcionados.
        - Verifica si los tipos ya existen en la base de datos; si no, realiza una
        solicitud externa para obtener la información
          del tipo y crea un nuevo registro de tipo.
        - Elimina los registros de tipos existentes en la base de datos que pertenecen
        al Pokémon especificado.
        - Agrega los nuevos registros de tipos a la base de datos.
        - Devuelve una lista de esquemas de tipos actualizados del Pokémon.

        Args:
            - types (Union[List[int], List[str]]): Una lista de IDs o nombres de tipos
            proporcionados en la solicitud.
            - pokemon_id (int): El ID del Pokémon al que pertenecen los tipos.

        Returns:
            - List[PokemonTypeSchema]: Una lista de esquemas de tipos actualizados
            del Pokémon.


        """
        types_saved: List[Type] = []
        for _type in types:
            type_from_db = self._get_type_from_db(id=str(_type))
            if not type_from_db:
                try:
                    type_from_api = await fetch_type(
                        client=self.client,
                        id=_type,
                        response_class=TypeApiResponse,
                    )
                except Exception as e:
                    raise Exception(f'Tipo {_type} no encontrada.') from e
                if not type_from_api:
                    raise Exception(f'Tipo {_type} no encontrada.')
                type_from_db = Type(
                    name=type_from_api.name,
                    internal_id=type_from_api.id,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )  # type: ignore
                self.session.add(type_from_db)
                self.session.flush()
            types_saved.append(
                PokemonType(
                    pokemon_id=pokemon_id, type_id=type_from_db.id
                )  # type: ignore
            )
        self.session.query(PokemonType).filter(
            PokemonType.pokemon_id == pokemon_id
        ).delete()
        self.session.add_all(types_saved)
        self.session.flush()
        return [
            PokemonTypeSchema(
                id=_type.type.internal_id,  # type: ignore
                name=_type.type.name,  # type: ignore
            )
            for _type in types_saved
        ]

    def _update_sprites(
        self, sprites: List[PokemonSpriteInput], pokemon_id: int
    ) -> List[PokemonSpriteSchema]:
        """
        Actualiza los sprites de un Pokémon en la base de datos.

        Este método realiza las siguientes acciones:
        - Crea instancias de registros de sprites (Sprite) a partir de los detalles
        de sprites proporcionados.
        - Elimina los registros de sprites existentes en la base de datos que
        pertenecen al Pokémon especificado.
        - Agrega los nuevos registros de sprites a la base de datos.
        - Devuelve una lista de esquemas de sprites actualizados del Pokémon.

        Args:
            - sprites (List[PokemonSpriteInput]): Una lista de detalles de sprites
            proporcionados en la solicitud.
            - pokemon_id (int): El ID del Pokémon al que pertenecen los sprites.

        Returns:
            - List[PokemonSpriteSchema]: Una lista de esquemas de sprites actualizados
            del Pokémon.
        """
        sprites_saved: List[Sprite] = []
        for sprite in sprites:
            sprites_saved.append(
                Sprite(
                    pokemon_id=pokemon_id,
                    sprite_type=sprite.type,
                    url=sprite.url,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )  # type: ignore
            )
        self.session.query(Sprite).filter(
            Sprite.pokemon_id == pokemon_id
        ).delete()
        self.session.add_all(sprites_saved)
        return [
            PokemonSpriteSchema(
                type=sprite.sprite_type, url=sprite.url  # type: ignore
            )
            for sprite in sprites_saved
        ]

    async def get_response(
        self, id: str, body: PokemonInput
    ) -> PokemonResponse:
        """
        Obtiene y actualiza la respuesta detallada de un Pokémon.

        Este método toma como entrada el ID del Pokémon a actualizar (id) y los
        nuevos detalles del Pokémon proporcionados en el cuerpo (body). Luego,
        realiza la actualización de los detalles del Pokémon en la base de datos
        y devuelve una respuesta detallada del Pokémon actualizado.

        Args:
            - id (str): El ID del Pokémon a actualizar.
            - body (PokemonInput): Los nuevos detalles del Pokémon proporcionados
            en el cuerpo de la solicitud.

        Returns:
            - PokemonResponse: Un objeto que contiene la respuesta detallada del
            Pokémon actualizado.
        """
        pokemon = self._get_pokemon_from_db(id=id)
        if body.name:
            pokemon.name = body.name
        if body.abilities or len(body.abilities) > 0:  # type: ignore
            abilities = await self._update_abilities(abilities=body.abilities, pokemon_id=pokemon.id)  # type: ignore
        else:
            abilities = []
        if body.types or len(body.types) > 0:  # type: ignore
            types = await self._update_types(types=body.types, pokemon_id=pokemon.id)  # type: ignore
        else:
            types = []
        if body.sprites or len(body.sprites) > 0:  # type: ignore
            sprites = self._update_sprites(sprites=body.sprites, pokemon_id=pokemon.id)  # type: ignore
        else:
            sprites = []
        self.session.commit()
        return PokemonResponse(
            id=pokemon.pokemon_id,
            name=pokemon.name,
            abilities=abilities,
            types=types,
            sprites=sprites,
        )


async def update_specific_pokemon(
    id: str,
    body: PokemonInput,
    client: AsyncClient,
    session: Session,
) -> PokemonResponse:
    """
    Actualiza un Pokémon específico en la base de datos.

    Esta función toma como entrada el ID del Pokémon a actualizar (id), los nuevos
    detalles del Pokémon proporcionados en el cuerpo (body), un cliente asincrónico
    (client) para realizar solicitudes externas y una sesión de base de datos
    (session) para interactuar con la base de datos.

    Args:
        - id (str): El ID del Pokémon a actualizar.
        - body (PokemonInput): Los nuevos detalles del Pokémon proporcionados en
        el cuerpo de la solicitud.
        - client (AsyncClient): Un cliente asincrónico utilizado para realizar
        solicitudes externas.
        - session (Session): Una sesión de base de datos utilizada para interactuar
        con la base de datos.

    Returns:
        - PokemonResponse: Un objeto que contiene la respuesta de la actualización
        del Pokémon.
    """
    service = PokemonSpecificUpdateService(client=client, session=session)
    return await service.get_response(id=id, body=body)
