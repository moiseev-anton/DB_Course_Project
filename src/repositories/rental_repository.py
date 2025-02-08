from .base_repository import SQLAlchemyRepository
from models import Rental, RentalStatus
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import joinedload
from sqlalchemy import select


class RentalsRepository(SQLAlchemyRepository[Rental, int]):
    model = Rental

    async def get_current_rental(self, user_id: UUID) -> Rental:
        result = await self.session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .where(
                (self.model.status == RentalStatus.ACTIVE) |
                (self.model.status == RentalStatus.PENDING)
            )
            .options(joinedload(self.model.scooter))
        )
        return result.scalar_one_or_none()
