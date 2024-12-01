from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_USER_PASSWORD: str
    SECRET_KEY: str
    ALGORTIHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self):
        url = (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_USER_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )
        return url

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
