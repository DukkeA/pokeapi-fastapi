from typing import Sequence

from pydantic import BaseModel


class PokemonAbility(BaseModel):
    id: int
    name: str


class PokemonType(BaseModel):
    id: int
    name: str


class PokemonSprite(BaseModel):
    id: int
    type: str
    url: str


class Pokemon(BaseModel):
    id: int
    name: str
    abilities: Sequence[PokemonAbility]
    types: Sequence[PokemonType]
    sprites: Sequence[PokemonSprite]
