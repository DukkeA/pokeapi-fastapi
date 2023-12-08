from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.lib.database.base import Base
from src.lib.database.mixins import (
    IntegerIdMixin,
    IsActiveMixin,
    TimestampMixin,
)


class SpriteType(Enum):
    DEFAULT = "default"
    DREAM_WORLD = "dream_world"
    HOME = "home"
    OFFICIAL_ARTWORK = "official-artwork"


class Sprite(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "sprites"
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"))
    sprite_type: Mapped[SpriteType]
    url: Mapped[str]
