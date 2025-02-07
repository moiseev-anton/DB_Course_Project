from typing import List, Optional

from models import ScooterStatus
from schemas import ScooterDisplay
from unitofwork import IUnitOfWork


class ScooterService:
    @staticmethod
    async def get_available_scooter(uow: IUnitOfWork, scooter_id: int) -> ScooterDisplay:
        async with uow:
            scooter = await uow.scooters.get_available_scooter(id=scooter_id)
            if not scooter:
                raise ValueError("Самокат не найден")
            return ScooterDisplay.model_validate(scooter)

    @staticmethod
    async def get_available_scooters(
        uow: IUnitOfWork,
        location_id: Optional[int] = None,
        min_battery: Optional[int] = None
    ) -> List[ScooterDisplay]:
        async with uow:
            scooters = await uow.scooters.get_available_scooters(location_id, min_battery)
            return [ScooterDisplay.model_validate(s) for s in scooters]
