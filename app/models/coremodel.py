from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

Base = DeclarativeBase

timestamp_created_at = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=func.now())
]

timestamp_updated_at = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=func.now(), onupdate=func.now())
]


class CoreModel(Base):
    __abstract__ = True

    id: Mapped[Annotated[int, mapped_column(primary_key=True, index=True)]]
    created_time = Mapped[timestamp_created_at]
    updated_at = Mapped[timestamp_updated_at]
