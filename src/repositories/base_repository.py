from abc import ABC, abstractmethod
from functools import wraps
from typing import Type, List, Optional, Dict

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


def check_model_set(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        if self.model is None:
            raise ValueError("Model is not set")
        return await method(self, *args, **kwargs)

    return wrapper


class AbstractRepository[IDType](ABC):
    @abstractmethod
    async def get_one(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: IDType, obj_data):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: IDType):
        raise NotImplementedError


class SQLAlchemyRepository[T, IDType](AbstractRepository[IDType]):
    model: Optional[Type[T]]

    def __init__(self, session: AsyncSession):
        self.session = session

    @check_model_set
    async def get_one(self, **filter_by) -> Optional[T]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_one_with_related(
        self,
        filter_by: Optional[List] = None,
        options: Optional[List] = None
    ) -> Optional[T]:
        query = select(self.model).filter(*filter_by) if filter_by else select(self.model)
        if options:
            query = query.options(*options)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    @check_model_set
    async def get_all(self, **filter_by) -> List[T]:
        query = select(self.model)
        if filter_by:
            query = query.filter_by(**filter_by)

        result = await self.session.execute(query)
        return list(result.scalars())

    async def get_all_with_related(
        self,
        filter_by: Optional[List] = None,
        options: Optional[List] = None
    ) -> List[T]:
        query = select(self.model)
        if filter_by:
            query = query.filter(*filter_by)
        if options:
            query = query.options(*options)
        result = await self.session.execute(query)
        return list(result.scalars())

    @check_model_set
    async def create_one(self, data: dict) -> T:
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    @check_model_set
    async def update_one(self, id: IDType, data: dict) -> T:
        query = update(self.model).values(**data).filter_by(id=id).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    @check_model_set
    async def delete_one(self, id: IDType) -> None:
        query = delete(self.model).filter_by(id=id)
        await self.session.execute(query)
