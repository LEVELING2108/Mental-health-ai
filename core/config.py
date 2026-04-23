from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Mental Health AI Enterprise API"
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = "model/model.pkl"
    VECTORIZER_PATH: str = "model/vectorizer.pkl"
    DATA_PATH: str = "data/dataset.csv"
    LOG_LEVEL: str = "INFO"

    # Database Settings
    DATABASE_URL: str = "sqlite:///./mental_health.db"

    # Security Settings (In production, replace SECRET_KEY via .env)
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 Days


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
