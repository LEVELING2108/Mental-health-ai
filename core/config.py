from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Mental Health AI Support API"
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = "model/model.pkl"
    VECTORIZER_PATH: str = "model/vectorizer.pkl"
    DATA_PATH: str = "data/dataset.csv"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
