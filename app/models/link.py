from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .basemodel import BaseModel

str_265 = Annotated[str, mapped_column(String(265))]


class Link(BaseModel):
    __tablename__ = "links"

    long_url: Mapped[str_265] = mapped_column(nullable=False, index=True)
    short_url: Mapped[str_265] = mapped_column(nullable=False, index=True, unique=True)
    visits: Mapped[int] = mapped_column(nullable=False, default=0)

    def __repr__(self):
        return f"<Link(long_url={self.long_url}, short_url={self.short_url}, visits={self.visits})>"
