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
    access_token_expire_minutes: int
    
    model_config = SettingsConfigDict(env_file=".env")

# This lru cache singleton pattern to ensure that the settings are loaded only once
@lru_cache
def get_settings():
    return Settings()

settings = get_settings()