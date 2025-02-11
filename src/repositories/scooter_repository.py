from typing import Optional, List

from sqlalchemy import Sequence, select, func, RowMapping, and_
from sqlalchemy.orm import joinedload

from models import Scooter, ScooterStatus, Rental, RentalStatus
from .base_repository import SQLAlchemyRepository
from datetime import timedelta


class ScootersRepository(SQLAlchemyRepository[Scooter, int]):
    model = Scooter

    async def get_available_scooter(self, id: int) -> Scooter:

        filters = [
            self.model.id == id,
            self.model.status == ScooterStatus.AVAILABLE,
        ]

        options = [joinedload(self.model.location), joinedload(self.model.tariff)]

        return await self.get_one_with_related(filter_by=filters, options=options)

    async def get_available_scooters(
        self, location_id: Optional[int] = None, min_battery: Optional[int] = None
    ) -> Sequence[Scooter]:

        filters = [
            self.model.status == ScooterStatus.AVAILABLE,
        ]

        if location_id:
            filters.append(self.model.location_id == location_id)

        if min_battery:
            filters.append(self.model.battery_level >= min_battery)

        options = [joinedload(self.model.location), joinedload(self.model.tariff)]

        return await self.get_all_with_related(filter_by=filters, options=options)

    async def get_scooter_stats(self, start_date, end_date) -> List[dict]:
        end_date = end_date + timedelta(days=1)
        query = (
            select(
                self.model.id,
                self.model.model,
                func.count(Rental.id).label("total_rentals"),
                func.sum(Rental.duration).label("total_duration"),
                func.sum(Rental.total_price).label("total_revenue"),
                func.avg(self.model.battery_level).label("avg_battery_after"),
            )
            .join(Rental)
            .where(
                and_(
                    Rental.status == RentalStatus.COMPLETED,
                    Rental.created_at.between(start_date, end_date),
                )
            )
            .group_by(self.model.id, self.model.model)
        )
        result = await self.session.execute(query)
        return result.mappings().all()
