from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.lib.database.base import Base
from src.lib.database.mixins import IntegerIdMixin, IsActiveMixin, TimestampMixin

if TYPE_CHECKING:
    from . import Ability, Type


class Pokemon(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "pokemons"
    pokemon_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    abilities: Mapped[List["PokemonAbility"]] = relationship(
        back_populates="pokemon"
    )
    types: Mapped[List["PokemonType"]] = relationship(back_populates="pokemon")


class PokemonAbility(IntegerIdMixin, Base):
    __tablename__ = "pokemon_abilities"
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"))
    ability_id: Mapped[int] = mapped_column(ForeignKey("abilities.id"))
    pokemon: Mapped["Pokemon"] = relationship(back_populates="abilities")
    ability: Mapped["Ability"] = relationship()


class PokemonType(IntegerIdMixin, Base):
    __tablename__ = "pokemon_types"
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("types.id"))
    pokemon: Mapped["Pokemon"] = relationship(back_populates="types")
    type: Mapped["Type"] = relationship()
