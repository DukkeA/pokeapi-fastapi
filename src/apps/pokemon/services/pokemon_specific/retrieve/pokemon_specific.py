from typing import Optional, Sequence

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import Session, contains_eager

from ....models import (
    Ability,
    Pokemon,
    PokemonAbility,
    PokemonType,
    Sprite,
    Type,
)
from ....schemas.pokemon_detailed.base import Pokemon as PokemonBase
from ....schemas.pokemon_detailed.base import (
    PokemonAbility as PokemonAbilityBase,
)
from ....schemas.pokemon_detailed.base import (
    PokemonSprite as PokemonSpriteBase,
)
from ....schemas.pokemon_detailed.base import PokemonType as PokemonTypeBase
from .pokemon_ability import PokemonAbilityService
from .pokemon_sprite import PokemonSpriteService
from .pokemon_type import PokemonTypeService


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
        if len(sprites) < 4:
            service = PokemonSpriteService(
                client=self.client, session=self.session
            )
            sprites = await service.update_sprites(pokemon=pokemon)
        self.session.commit()
        return PokemonBase(
            id=pokemon.pokemon_id,
            name=pokemon.name,
            abilities=abilities,
            types=types,
            sprites=sprites,
        )


async def get_specific_pokemon(
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
