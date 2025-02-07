from typing import List

from models import ScooterStatus, RentalStatus
from schemas import RentalDisplay
from unitofwork import IUnitOfWork
from sqlalchemy.dialects.postgresql import UUID


class RentalService:
    async def create_rental(
            self,
            uow: IUnitOfWork,
            user_id: UUID,
            scooter_id: int,
            unit_count: int
    ) -> RentalDisplay:
        async with uow:
            # Получаем самокат
            scooter = await uow.scooters.get_available_scooter(id=scooter_id)
            if not scooter or scooter.status != ScooterStatus.AVAILABLE:
                raise ValueError("Самокат недоступен для аренды")

            # Проверяем, что пользователь не имеет активной аренды
            active_rental = await uow.rentals.get_one(
                {"user_id": user_id,
                 "status": RentalStatus.ACTIVE}
            )
            if active_rental:
                raise ValueError("У вас уже есть активная аренда")

            # Рассчитываем стоимость
            tariff = scooter.tariff
            total_price = tariff.price * unit_count

            # Создаем аренду
            rental_data = RentalCreate(
                user_id=user_id,
                scooter_id=scooter_id,
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=hours),
                total_price=total_price,
                status=RentalStatus.ACTIVE
            )
            rental = await uow.rentals.create_one(rental_data.model_dump())

            # Обновляем статус самоката
            await uow.scooters.update_one(
                id=scooter_id,
                data={"status": ScooterStatus.RENTED}
            )

            await uow.commit()
            return RentalDisplay.model_validate(rental)
