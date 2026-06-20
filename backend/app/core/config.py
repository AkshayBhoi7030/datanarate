from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "DataNarrate"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    SECRET_KEY: str = "your-super-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/datanarrate"
    REDIS_URL: str = "redis://localhost:6379/0"

    CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:5173", "http://localhost:3000"]

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Phase 3 - AI Settings
    # OpenRouter Settings (Primary)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-oss-20b:free"
    OPENROUTER_TIMEOUT: int = 60
    OPENROUTER_MAX_RETRIES: int = 3
    
    # Ollama Settings (Fallback/Optional)
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "phi3:mini"
    OLLAMA_TIMEOUT: int = 60
    OLLAMA_MAX_RETRIES: int = 3

    CHROMADB_PERSIST_DIR: str = "./.chromadb"
    CHROMADB_COLLECTION: str = "datanarrate_schema"

    CACHE_TTL_SQL: int = 3600
    CACHE_TTL_RESULTS: int = 3600
    CACHE_TTL_INSIGHTS: int = 3600

    # Phase 8 - OAuth Settings
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/github/callback"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
