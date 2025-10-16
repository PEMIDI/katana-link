from collections.abc import Generator
from sqlalchemy.orm import Session

from ..db.session import AsyncSessionLocal


def get_db() -> Generator[Session, None, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
