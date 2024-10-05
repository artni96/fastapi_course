from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_USER_PASSWORD: str
    SECRET_KEY: str
    ALGORTIHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DB_URL(self):
        url = (
            f'postgresql+asyncpg://{self.DB_USER}:'
            f'{self.DB_USER_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/'
            f'{self.DB_NAME}'
        )
        return url

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
