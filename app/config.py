from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str
    redis_url: str
    telegram_bot_token: str
    export_files_ttl_hours: int = 24
    search_cache_ttl_seconds: int = 900
    default_language: str = "ru"
    enabled_sources: list[str] = [
        "mangalib",
        "mangabuff",
        "remanga",
        "senkuro",
        "dezu",
        "mangachan",
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("enabled_sources", mode="before")
    @classmethod
    def parse_sources(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


settings = Settings()
