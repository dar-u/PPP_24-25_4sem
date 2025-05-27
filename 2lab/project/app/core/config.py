from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "your-secret-key"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

