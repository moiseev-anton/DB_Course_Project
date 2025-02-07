from .base_repository import SQLAlchemyRepository
from models import Rental


class RentalsRepository(SQLAlchemyRepository[Rental, int]):
    model = Rental
