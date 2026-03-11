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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
