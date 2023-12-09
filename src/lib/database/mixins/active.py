from sqlalchemy.orm import Mapped, mapped_column


class IsActiveMixin:
    active: Mapped[bool] = mapped_column(default=True)
