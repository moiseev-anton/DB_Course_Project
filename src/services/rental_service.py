from sqlalchemy.dialects.postgresql import UUID

from schemas import (
    RentalDisplay,
    RentalCreate,
    RentalInfoDisplay,
    RentalReport,
    DateRange,
    FinancialReport,
)
from unitofwork import IUnitOfWork
from datetime import datetime
from typing import Optional, List
from models import RentalStatus


class RentalService:
    async def create_rental(
        self,
        uow: IUnitOfWork,
        user_id: UUID,
        scooter_id: int,
        form_data: RentalCreate,
    ) -> int:
        async with uow:
            # Получаем самокат
            scooter = await uow.scooters.get_available_scooter(id=scooter_id)
            if not scooter:
                raise ValueError("Самокат недоступен для аренды")

            # Проверяем, что пользователь не имеет активной аренды
            current_rental = await self.get_current_rental(uow, user_id=user_id)
            if current_rental:
                raise ValueError("У вас уже есть аренда")

            # Рассчитываем стоимость
            tariff = scooter.tariff
            duration = tariff.unit * form_data.unit_count
            total_price = tariff.price * form_data.unit_count

            # Создаем аренду
            rental_data = {
                "user_id": user_id,
                "scooter_id": scooter_id,
                "duration": duration,
                "total_price": total_price,
            }
            rental = await uow.rentals.create_one(rental_data)

            await uow.commit()
            return rental.id

    async def get_current_rental(
        self, uow: IUnitOfWork, user_id: UUID
    ) -> Optional[RentalDisplay]:
        async with uow:
            rental = await uow.rentals.get_current_rental(user_id=user_id)
            if rental:
                if rental.end_time is not None and rental.end_time < datetime.now():
                    await uow.rentals.update_one(
                        id=rental.id, data={"status": RentalStatus.COMPLETED}
                    )
                    await uow.commit()
                    return None
                return RentalDisplay(
                    id=rental.id,
                    scooter_model=rental.scooter.model,
                    scooter_battery_level=rental.scooter.battery_level,
                    status=rental.status.value,
                    end_time=rental.end_time,
                    duration=(int(rental.duration.total_seconds()) // 60),
                    total_price=rental.total_price,
                    remaining_time=(
                        int((rental.end_time - datetime.now()).total_seconds())
                        if rental.end_time
                        else None
                    ),
                )

    async def pay_rent(self, uow: IUnitOfWork, rental_id: int) -> None:
        async with uow:
            rental = await uow.rentals.get_one(id=rental_id)
            if not rental:
                raise ValueError("Аренда не доступна")

            await uow.payments.create_one(
                {"rental_id": rental_id, "amount": rental.total_price}
            )
            end_time = datetime.now() + rental.duration
            await uow.rentals.update_one(
                id=rental_id, data={"status": RentalStatus.ACTIVE, "end_time": end_time}
            )
            await uow.commit()

    async def cancel_rent(self, uow: IUnitOfWork, rental_id: int) -> None:
        async with uow:
            await uow.rentals.update_one(
                id=rental_id, data={"status": RentalStatus.CANCELLED}
            )
            await uow.commit()

    async def get_user_rental_history(
        self, uow: IUnitOfWork, user_id: UUID, status: Optional[str] = None
    ) -> List[RentalInfoDisplay]:
        async with uow:
            rentals = await uow.rentals.get_user_rentals(user_id=user_id, status=status)
            return [RentalInfoDisplay.model_validate(r) for r in rentals]

    async def get_stats(self, uow: IUnitOfWork, date_range: DateRange) -> RentalReport:
        async with uow:
            rental_stats = await uow.rentals.get_rental_stats(
                date_range.start_date, date_range.end_date
            )

            daily_income = await uow.rentals.get_daily_income(
                date_range.start_date, date_range.end_date
            )
            rental_stats["daily_income"] = daily_income

            return RentalReport(**rental_stats)

    async def get_financial_report(
        self, uow: IUnitOfWork, date_range: DateRange
    ) -> FinancialReport:
        async with uow:
            status_stats = await uow.rentals.get_financial_stats(
                date_range.start_date, date_range.end_date
            )

            report = FinancialReport()

            for status, count, amount in status_stats:
                if status in (RentalStatus.ACTIVE, RentalStatus.COMPLETED):
                    report.total_income += amount
                    report.total_rentals += count
                elif status == RentalStatus.PENDING:
                    report.pending_payments += amount
                    report.total_rentals += count
                elif status == RentalStatus.CANCELLED:
                    report.canceled_rentals += count
                    report.total_rentals += count

            return report
