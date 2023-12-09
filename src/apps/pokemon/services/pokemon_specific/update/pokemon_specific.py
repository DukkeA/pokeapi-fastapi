from httpx import AsyncClient
from sqlalchemy.orm import Session
from ....schemas.pokemon_detailed.base.pokemon import (
    PokemonInput,
    Pokemon as PokemonResponse,
)


class PokemonSpecificUpdateService:
    def __init__(self, client: AsyncClient, session: Session):
        self.client = client
        self.session = session

    async def get_response(
        self, id: str, body: PokemonInput
    ) -> PokemonResponse:
        return PokemonResponse(
            id=1,
            name='Test',
            abilities=[],
            types=[],
            sprites=[],
        )


async def update_specific_pokemon(
    id: str,
    body: PokemonInput,
    client: AsyncClient,
    session: Session,
) -> PokemonResponse:
    service = PokemonSpecificUpdateService(client=client, session=session)
    return await service.get_response(id=id, body=body)
