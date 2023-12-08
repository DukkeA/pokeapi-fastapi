from datetime import datetime
from typing import Optional, Sequence

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import Session, contains_eager

from src.commons.fetch import fetch_pokemon

from ..models import (
    Ability,
    Pokemon,
    PokemonAbility,
    PokemonType,
    Sprite,
    Type,
)
from ..schemas.pokemon_detailed.api import Pokemon as PokemonResponseApi
from ..schemas.pokemon_detailed.base import Pokemon as PokemonBase
from ..schemas.pokemon_detailed.base import (
    PokemonAbility as PokemonAbilityBase,
)
from ..schemas.pokemon_detailed.base import PokemonSprite as PokemonSpriteBase
from ..schemas.pokemon_detailed.base import PokemonType as PokemonTypeBase


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


class PokemonSpecificService:
    """
    Servicio para obtener detalles específicos de un Pokémon desde la base de datos
    y la API.

    Args:
        - client (AsyncClient): Cliente HTTP asincrónico para realizar solicitudes a la API.
        - session (Session): Sesión de la base de datos SQLAlchemy para realizar consultas.

    Methods:
        - get_response(id: str) -> Optional[PokemonBase]:
        Obtiene detalles específicos de un Pokémon.
        - _get_pokemon_base(id: str) -> Optional[Pokemon]:
        Obtiene un Pokémon de la base de datos según su ID o nombre.
        - _get_pokemon_abilities(id: int) -> Sequence[PokemonAbilityBase]:
        Obtiene las habilidades de un Pokémon a partir de su ID.
        - _get_pokemon_types(id: int) -> Sequence[PokemonTypeBase]:
        Obtiene los tipos de un Pokémon a partir de su ID.
        - _get_pokemon_sprites(id: int) -> Sequence[PokemonSpriteBase]:
        Obtiene los sprites de un Pokémon a partir de su ID.
        - _get_from_db(id: str) -> Optional[PokemonBase]:
        Obtiene detalles completos de un Pokémon desde la base de datos.

    """

    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    async def get_response(self, id: str) -> Optional[PokemonBase]:
        """
        Obtiene detalles específicos de un Pokémon.

        Args:
            - id (str): El ID del Pokémon que se desea obtener.

        Returns:
            - Optional[PokemonBase]: Detalles específicos del Pokémon o `None`
            si no se encuentra.
        """
        pokemon = await self._get_from_db(id=id)
        return pokemon

    def _get_pokemon_base(self, id: str) -> Optional[Pokemon]:
        """
        Obtiene un Pokémon de la base de datos según su ID o nombre.

        Esta función realiza una consulta a la base de datos para obtener un Pokémon
        específico, ya sea por su ID numérico o por su nombre. Si se proporciona un ID
        numérico, se buscará en la columna 'pokemon_id'. Si se proporciona un nombre,
        se buscará en la columna 'name'.

        Args:
            - id (str): El ID numérico o nombre del Pokémon que se desea obtener.

        Returns:
            - Optional[Pokemon]: Un objeto Pokémon o `None` si no se encuentra.
        """
        query = select(Pokemon)
        if id.isnumeric():
            query = query.filter(Pokemon.pokemon_id == id)
        else:
            query = query.filter(Pokemon.name == id)
        result = self.session.execute(query).scalars().first()
        return result

    def _get_pokemon_abilities(self, id: int) -> Sequence[PokemonAbilityBase]:
        """
        Obtiene las habilidades de un Pokémon a partir de su ID.

        Esta función realiza una consulta a la base de datos para obtener las
        habilidades de un Pokémon específico identificado por su ID numérico.
        Las habilidades se obtienen como objetos `PokemonAbilityBase`, que contienen
        el ID y el nombre de cada habilidad.

        Args:
            - id (int): El ID numérico del Pokémon del que se desean obtener las
            habilidades.

        Returns:
            - Sequence[PokemonAbilityBase]: Una secuencia de objetos `PokemonAbilityBase`
            que representan las habilidades del Pokémon.
        """
        query = (
            select(PokemonAbility)
            .join(Ability, PokemonAbility.ability_id == Ability.id)
            .options(contains_eager(PokemonAbility.ability))
            .filter(PokemonAbility.pokemon_id == id)
        )
        rows = self.session.execute(query).scalars().all()
        result: Sequence[PokemonAbilityBase] = []
        for row in rows:
            result.append(
                PokemonAbilityBase(
                    id=row.ability.internal_id,
                    name=row.ability.name,
                )
            )
        return result

    def _get_pokemon_types(self, id: int) -> Sequence[PokemonTypeBase]:
        """
        Obtiene los tipos de un Pokémon a partir de su ID.

        Esta función realiza una consulta a la base de datos para obtener los tipos
        de un Pokémon específico identificado por su ID numérico. Los tipos se obtienen
        como objetos `PokemonTypeBase`, que contienen el ID y el nombre de cada tipo.

        Args:
            - id (int): El ID numérico del Pokémon del que se desean obtener los tipos.

        Returns:
            - Sequence[PokemonTypeBase]: Una secuencia de objetos `PokemonTypeBase`
            que representan los tipos del Pokémon.
        """
        query = (
            select(PokemonType)
            .join(Type, PokemonType.type_id == Type.id)
            .options(contains_eager(PokemonType.type))
            .filter(PokemonType.pokemon_id == id)
        )
        rows = self.session.execute(query).scalars().all()
        result: Sequence[PokemonTypeBase] = []
        for row in rows:
            result.append(
                PokemonTypeBase(
                    id=row.type.internal_id,
                    name=row.type.name,
                )
            )
        return result

    def _get_pokemon_sprites(self, id: int) -> Sequence[PokemonSpriteBase]:
        """
        Obtiene los sprites de un Pokémon a partir de su ID.

        Esta función realiza una consulta a la base de datos para obtener los sprites
        asociados a un Pokémon específico identificado por su ID numérico. Los sprites
        se obtienen como objetos `PokemonSpriteBase`, que contienen el ID, el tipo y la URL
        de cada sprite.

        Args:
            - id (int): El ID numérico del Pokémon del que se desean obtener los sprites.

        Returns:
            - Sequence[PokemonSpriteBase]: Una secuencia de objetos `PokemonSpriteBase`
            que representan los sprites del Pokémon.
        """
        query = select(Sprite).filter(Sprite.pokemon_id == id)
        rows = self.session.execute(query).scalars().all()
        result: Sequence[PokemonSpriteBase] = []
        for row in rows:
            result.append(
                PokemonSpriteBase(
                    id=row.id,
                    type=row.sprite_type.value,
                    url=row.url,
                )
            )
        return result

    async def _get_from_db(self, id: str) -> Optional[PokemonBase]:
        """
        Obtiene detalles completos de un Pokémon desde la base de datos.

        Esta función busca un Pokémon en la base de datos identificado por su ID o nombre y
        recopila todos los detalles disponibles del Pokémon, incluyendo sus habilidades,
        tipos y sprites. Si el Pokémon no se encuentra en la base de datos, se realizan
        solicitudes a la API para obtener y actualizar esta información. Los detalles del
        Pokémon se devuelven como un objeto `PokemonBase`.

        Args:
            - id (str): El ID numérico o el nombre del Pokémon que se desea obtener.

        Returns:
            - Optional[PokemonBase]: Un objeto que contiene detalles completos del Pokémon
            si se encuentra en la base de datos o si se obtiene de la API. Si el Pokémon
            no se encuentra o si ocurre un error, se devuelve `None`.
        """
        pokemon = self._get_pokemon_base(id)
        if not pokemon:
            return None
        abilities = self._get_pokemon_abilities(pokemon.id)
        if not abilities:
            service = PokemonAbilityService(
                client=self.client, session=self.session
            )
            abilities = await service.update_abilities(pokemon=pokemon)
        types = self._get_pokemon_types(pokemon.id)
        if not types:
            service = PokemonTypeService(
                client=self.client, session=self.session
            )
            types = await service.update_types(pokemon=pokemon)
        sprites = self._get_pokemon_sprites(pokemon.id)
        self.session.commit()
        return PokemonBase(
            id=pokemon.pokemon_id,
            name=pokemon.name,
            abilities=abilities,
            types=types,
            sprites=sprites,
        )


async def get_spacific_pokemon(
    id: str,
    client: AsyncClient,
    session: Session,
) -> Optional[PokemonBase]:
    """
    Obtiene detalles específicos de un Pokémon.

    Esta función delega la obtención de detalles específicos de un Pokémon a un
    servicio especializado. Se encarga de llamar al servicio correspondiente
    utilizando el cliente HTTP proporcionado en la solicitud y la sesión de base
    de datos especificada.

    Args:
        - id (str): El ID del Pokémon que se desea obtener.
        - client (AsyncClient): El cliente HTTP asincrónico utilizado para realizar
        la solicitud a la API.
        - session (Session): La sesión de base de datos a utilizar para recuperar
        los datos del Pokémon.

    Returns:
        - Optional[PokemonBase]: Un objeto que contiene detalles específicos del
        Pokémon obtenidos desde la API o `None` si el Pokémon no se encuentra o
        la solicitud falla.
    """
    service = PokemonSpecificService(client=client, session=session)
    return await service.get_response(id=id)
