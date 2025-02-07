from .base_repository import SQLAlchemyRepository
from models import User
from sqlalchemy.dialects.postgresql import UUID


class UsersRepository(SQLAlchemyRepository[User, UUID]):
    model = User
