import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "TubeShield AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None

    # LLM Settings
    DEFAULT_LLM_PROVIDER: str = "openai" # "openai" or "gemini"
    DEFAULT_MODEL_NAME: str = "gpt-4o-mini"

    # Database Settings
    DATABASE_URL: str = "sqlite:///./tubeshield.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
