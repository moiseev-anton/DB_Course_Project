from typing import List

from schemas import LocationDisplay
from unitofwork import IUnitOfWork


class LocationService:
    async def get_all_locations(
            self,
            uow: IUnitOfWork,
    ) -> List[LocationDisplay]:
        async with uow:
            locations = await uow.locations.get_all()
            return [LocationDisplay.model_validate(l) for l in locations]
