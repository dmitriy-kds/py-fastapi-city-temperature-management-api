from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_name: str = "City temperature measurement"

    database_url: str | None = "sqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
