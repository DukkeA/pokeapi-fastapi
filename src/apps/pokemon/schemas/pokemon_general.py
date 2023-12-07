from typing import List, Optional

from pydantic import BaseModel


class PokemonGeneral(BaseModel):
    id: int
    name: str
    url: str


class PokemonGeneralApi(BaseModel):
    name: str
    url: str


class PokemonGeneralResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PokemonGeneral]


class PokemonGeneralApiResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PokemonGeneralApi]
