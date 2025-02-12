from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """Базовый класс для конфигурации."""

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    STATIC_DIR: str = os.path.join(os.path.dirname(__file__), "static")

    SECRET_KEY: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://user_name:password@host:5432/db_name
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_URL_psycopg2(self):
        # postgresql+psycopg2://user_name:password@host:5432/db_name
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", ".env")
    )


settings = Settings()


if __name__ == "__main__":
    print(settings.DATABASE_URL_asyncpg)
    print(settings.SECRET_KEY)
