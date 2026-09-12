from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

# Создаем синхронный движок SQLAlchemy
sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg2,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

session_maker = sessionmaker(sync_engine)

# Создаем асинхронный движок SQLAlchemy
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    """Общая база ORM-моделей и метаданных для Alembic."""

    pass
