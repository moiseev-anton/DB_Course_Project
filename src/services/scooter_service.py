from typing import List, Optional

from schemas import ScooterDisplay, DateRange, ScooterUsageReport
from unitofwork import IUnitOfWork


class ScooterService:
    @staticmethod
    async def get_available_scooter(
        uow: IUnitOfWork, scooter_id: int
    ) -> ScooterDisplay:
        async with uow:
            scooter = await uow.scooters.get_available_scooter(id=scooter_id)
            if not scooter:
                raise ValueError("Самокат не найден")
            return ScooterDisplay.model_validate(scooter)

    @staticmethod
    async def get_available_scooters(
        uow: IUnitOfWork,
        location_id: Optional[int] = None,
        min_battery: Optional[int] = None,
    ) -> List[ScooterDisplay]:
        async with uow:
            # Обновляем статусы истекших аренд
            await uow.rentals.update_expired_rentals_status()
            await uow.commit()

            scooters = await uow.scooters.get_available_scooters(
                location_id, min_battery
            )
            return [ScooterDisplay.model_validate(s) for s in scooters]

    async def get_usage_stats(
        self, uow: IUnitOfWork, date_range: DateRange
    ) -> List[ScooterUsageReport]:
        async with uow:
            usage_stats = await uow.scooters.get_scooter_stats(
                date_range.start_date, date_range.end_date
            )
        return [ScooterUsageReport(**row) for row in usage_stats]
