from typing import Optional, Sequence, Union

from pydantic import BaseModel


class PokemonAbility(BaseModel):
    id: int
    name: str


class PokemonType(BaseModel):
    id: int
    name: str


class PokemonSprite(BaseModel):
    type: str
    url: Optional[str]


class Pokemon(BaseModel):
    id: int
    name: str
    abilities: Sequence[PokemonAbility]
    types: Sequence[PokemonType]
    sprites: Sequence[PokemonSprite]


class PokemonSpriteInput(BaseModel):
    type: str
    url: Optional[str]


class PokemonInput(BaseModel):
    name: Optional[str]
    abilities: Optional[Union[Sequence[int], Sequence[str]]]
    types: Optional[Union[Sequence[int], Sequence[str]]]
    sprites: Optional[Sequence[PokemonSpriteInput]]
