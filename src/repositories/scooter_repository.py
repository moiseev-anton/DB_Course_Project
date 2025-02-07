from .base_repository import SQLAlchemyRepository
from models import Scooter, ScooterStatus
from typing import Optional, List
from sqlalchemy.orm import joinedload


class ScootersRepository(SQLAlchemyRepository[Scooter, int]):
    model = Scooter

    async def get_available_scooter(self, id: int) -> Scooter:

        filters = [self.model.id == id,
                   self.model.status == ScooterStatus.AVAILABLE,
                   ]

        options = [
            joinedload(self.model.location),
            joinedload(self.model.tariff)
        ]

        return await self.get_one_with_related(filter_by=filters, options=options)

    async def get_available_scooters(
            self,
            location_id: Optional[int] = None,
            min_battery: Optional[int] = None
    ) -> List[Scooter]:

        filters = [Scooter.status == ScooterStatus.AVAILABLE, ]

        if location_id:
            filters.append(Scooter.location_id == location_id)

        if min_battery:
            filters.append(Scooter.battery_level >= min_battery)

        options = [
            joinedload(Scooter.location),
            joinedload(Scooter.tariff)
        ]

        return await self.get_all_with_related(filter_by=filters, options=options)
