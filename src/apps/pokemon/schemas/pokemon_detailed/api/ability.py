from pydantic import BaseModel


class Ability(BaseModel):
    id: int
    name: str
