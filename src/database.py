from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from contextlib import asynccontextmanager, contextmanager

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
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


# Для синхронной сессии
@contextmanager
def get_sync_db():
    """Контекстный менеджер синхронной сессии с БД."""
    db: Session = session_maker()
    try:
        yield db
    finally:
        db.close()


# Для асинхронной сессии
@asynccontextmanager
async def get_async_db():
    """Контекстный менеджер для асинхронной сессии с БД."""
    async with async_session_maker() as db:  # async_session автоматически управляет сессией
        yield db
