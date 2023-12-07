from sqlalchemy.orm import Mapped, mapped_column

from src.lib.database.base import Base
from src.lib.database.mixins import IntegerIdMixin, IsActiveMixin, TimestampMixin


class Type(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "types"
    name: Mapped[str]
    internal_id: Mapped[int] = mapped_column(unique=True)
