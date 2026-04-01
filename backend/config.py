from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_ENV: str = "development"
    SECRET_KEY: str = "dev-secret-key"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    MONGODB_URI: str = "mongodb://localhost:27017/mandimitra"
    MONGODB_DB_NAME: str = "mandimitra"
    DATAGOV_API_KEY: str = ""
    UPSTASH_REDIS_URL: str = ""
    UPSTASH_REDIS_TOKEN: str = ""
    MODEL_PATH: str = "./ml/saved_models/lstm_attention_v1.pt"
    SCALER_PATH: str = "./ml/saved_models/scaler.pkl"
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
