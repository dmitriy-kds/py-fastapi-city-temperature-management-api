from functools import lru_cache

from app import settings
from app.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return settings.Settings()
