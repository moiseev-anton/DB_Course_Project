from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from datetime import timedelta
from authx import AuthXConfig


class Settings(BaseSettings):
    """Базовый класс для конфигурации."""
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    STATIC_DIR: str = os.path.join(os.path.dirname(__file__), "static")

    SECRET_KEY: str
    # JWT_ALGORITHM: str
    # JWT_ACCESS_TOKEN_EXPIRES: int
    # JWT_REFRESH_TOKEN_EXPIRES: int
    #
    # # Заголовки
    # JWT_HEADER_NAME: str
    # JWT_HEADER_TYPE: str
    #
    # # Cookies (только для refresh-токена)
    # JWT_REFRESH_COOKIE_NAME: str
    # JWT_REFRESH_COOKIE_PATH: str
    # JWT_COOKIE_SAMESITE: str
    # JWT_COOKIE_SECURE: bool
    #
    # # Автообновление refresh-токена
    # JWT_IMPLICIT_REFRESH_DELTATIME: int

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://user_name:password@host:5432/db_name
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def DATABASE_URL_psycopg2(self):
        # postgresql+psycopg2://user_name:password@host:5432/db_name
        return f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '..', '.env'))


settings = Settings()

# auth_config = AuthXConfig(
#     JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
#     JWT_ALGORITHM=settings.JWT_ALGORITHM,
#     JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES),
#     JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES),
#
#     # Access-токен передаётся в заголовке
#     JWT_HEADER_NAME=settings.JWT_HEADER_NAME,
#     JWT_HEADER_TYPE=settings.JWT_HEADER_TYPE,
#
#     # Refresh-токен хранится в HttpOnly Cookie
#     JWT_REFRESH_COOKIE_NAME=settings.JWT_REFRESH_COOKIE_NAME,
#     JWT_REFRESH_COOKIE_PATH=settings.JWT_REFRESH_COOKIE_PATH,
#     JWT_COOKIE_SAMESITE=settings.JWT_COOKIE_SAMESITE,
#     JWT_COOKIE_SECURE=settings.JWT_COOKIE_SECURE,
#
#     # Автообновление refresh-токена
#     JWT_IMPLICIT_REFRESH_DELTATIME=timedelta(minutes=settings.JWT_IMPLICIT_REFRESH_DELTATIME),
# )

# class DevelopmentConfig(Config):
#     """Конфигурация для разработки."""
#     DEBUG = True
#
#
# class ProductionConfig(Config):
#     """Конфигурация для продакшн среды."""
#     DEBUG = False
#     # Добавьте другие параметры для продакшн конфигурации, если нужно
#
#
# class TestingConfig(Config):
#     """Конфигурация для тестирования."""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"  # Пример для тестовой БД
#
#
# # Используем нужную конфигурацию в зависимости от окружения
# config = DevelopmentConfig  # или ProductionConfig, или TestingConfig

if __name__ == '__main__':
    print(settings.DATABASE_URL_asyncpg)
    print(settings.SECRET_KEY)
