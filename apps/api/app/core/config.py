from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Resume AI Analyst"
    secret_key: str = "change-me-in-production"
    access_token_minutes: int = 30
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/resume_ai"
    cors_origins: list[str] = ["http://localhost:3000"]
    upload_dir: str = "./uploads"
    max_upload_mb: int = 5
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
