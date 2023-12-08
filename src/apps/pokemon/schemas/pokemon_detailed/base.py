from typing import Optional, Sequence

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


class PokemonInput(BaseModel):
    name: Optional[str]


class PokemonAbilityInput(BaseModel):
    name: Optional[str]


class PokemonTypeInput(BaseModel):
    name: Optional[str]


class PokemonSpriteInput(BaseModel):
    url: Optional[str]
