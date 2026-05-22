from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "graduate-employment-platform"
    demo_mode: bool = True
    model_version: str = "random-forest-demo-v1"
    ai_enabled: bool = True
    zenmux_api_key: str = ""
    zenmux_base_url: str = "https://zenmux.ai/api/v1"
    zenmux_model: str = "google/gemini-3.5-flash-free"
    ai_timeout_seconds: int = 20
    mysql_url: str = Field(
        default="mysql+pymysql://root:root@localhost:3306/graduate_employment?charset=utf8mb4",
        description="SQLAlchemy MySQL connection string",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
