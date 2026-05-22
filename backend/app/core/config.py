from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "graduate-employment-platform"
    demo_mode: bool = True
    model_version: str = "random-forest-demo-v1"
    ai_enabled: bool = True
    ai_api_key: str = ""
    ai_base_url: str = "https://openrouter.ai/api/v1"
    ai_model: str = "openai/gpt-oss-120b:free"
    zenmux_api_key: str = ""
    zenmux_base_url: str = "https://zenmux.ai/api/v1"
    zenmux_model: str = "google/gemini-3.5-flash-free"
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openai/gpt-oss-120b:free"
    openrouter_app_name: str = "EmploySight"
    openrouter_site_url: str = ""
    ai_timeout_seconds: int = 20
    admin_username: str = "admin"
    admin_password: str = "admin123"
    admin_security_pepper: str = ""
    admin_delete_password_hash: str = ""
    admin_unban_password_hash: str = ""
    admin_delete_max_attempts: int = 3
    admin_delete_ban_minutes: int = 30
    audit_log_path: str = "data/admin_login_audit.jsonl"
    audit_backup_dir: str = "data/admin_login_backups"
    mysql_url: str = Field(
        default="mysql+pymysql://root:root@localhost:3306/graduate_employment?charset=utf8mb4",
        description="SQLAlchemy MySQL connection string",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
