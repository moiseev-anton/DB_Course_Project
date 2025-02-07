from .base_repository import SQLAlchemyRepository
from models import Location


class LocationsRepository(SQLAlchemyRepository[Location, int]):
    model = Location
