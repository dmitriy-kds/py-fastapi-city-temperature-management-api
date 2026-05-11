from functools import lru_cache
from typing import Iterator

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.settings import settings, Settings


def get_db() -> Iterator[Session] | None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@lru_cache
def get_settings() -> Settings:
    return settings
