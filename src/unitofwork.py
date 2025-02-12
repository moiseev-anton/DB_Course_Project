from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import async_session_maker
from repositories import (
    UsersRepository,
    ScootersRepository,
    RentalsRepository,
    PaymentsRepository,
    LocationsRepository,
)


class IUnitOfWork(ABC):
    session: AsyncSession | Session
    users: UsersRepository
    scooters: ScootersRepository
    rentals: RentalsRepository
    payments: PaymentsRepository
    locations: LocationsRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.async_session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.async_session_factory()

        # Репозитории для всех моделей
        self.users = UsersRepository(self.session)
        self.scooters = ScootersRepository(self.session)
        self.rentals = RentalsRepository(self.session)
        self.payments = PaymentsRepository(self.session)
        self.locations = LocationsRepository(self.session)
        return self  # Возвращаем экземпляр UnitOfWork для использования в контекстном менеджере

    async def __aexit__(self, *args):
        # Откатить транзакцию, если ошибка, и закрыть сессию
        await self.rollback()
        await self.session.close()

    async def commit(self):
        # Фиксируем все изменения в базе данных
        await self.session.commit()

    async def rollback(self):
        # Откатываем изменения, если ошибка
        await self.session.rollback()
