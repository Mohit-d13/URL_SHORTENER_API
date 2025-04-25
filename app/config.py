import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# Settings class to load and validate environment variables from .env file
class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")

# This lru cache singleton pattern to ensure that the settings are loaded only once
@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

def get_database_url():
    # First check for Render's DATABASE_URL
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        # Fix for Render's postgres:// vs postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url
    
    # Fall back to constructing from individual settings
    if settings.db_username and settings.db_password and settings.db_host and settings.db_name:
        return f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port or '5432'}/{settings.db_name}"
    
    # If we get here, we don't have database configuration
    raise ValueError("No database configuration found. Set DATABASE_URL or individual DB_ environment variables.")