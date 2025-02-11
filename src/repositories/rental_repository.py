from collections.abc import Sequence
from datetime import timedelta
from typing import Optional, Any

from sqlalchemy import select, func, Row, RowMapping, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import joinedload

from models import Rental, RentalStatus
from .base_repository import SQLAlchemyRepository
from datetime import datetime


class RentalsRepository(SQLAlchemyRepository[Rental, int]):
    model = Rental

    async def get_current_rental(self, user_id: UUID) -> Rental:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .where(
                (self.model.status == RentalStatus.ACTIVE)
                | (self.model.status == RentalStatus.PENDING)
            )
            .options(joinedload(self.model.scooter))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_rentals(
        self, user_id: UUID, status: Optional[str] = None
    ) -> Sequence[Rental]:
        query = select(self.model).where(self.model.user_id == user_id)
        if status is not None:
            query = query.where(self.model.status == status)
        query = query.order_by(self.model.end_time)
        query = query.options(joinedload(self.model.scooter))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_rental_stats(
        self, star_date, end_date
    ) -> dict[str, int | timedelta | float | None | list]:
        end_date = end_date + timedelta(days=1)
        query = select(
            func.count(self.model.id),
            func.avg(self.model.duration),
            func.sum(self.model.total_price),
        ).where(self.model.created_at.between(star_date, end_date))
        result = await self.session.execute(query)
        count, avg_duration, total_price = result.one()

        return {
            "total_rentals": count,
            "avg_duration": avg_duration,
            "total_revenue": total_price,
        }

    async def get_financial_stats(
        self, start_date, end_date
    ) -> Sequence[Row | RowMapping]:
        end_date = end_date + timedelta(days=1)

        # Статистика по статусам
        query = (
            select(
                self.model.status,
                func.count(self.model.id),
                func.coalesce(func.sum(self.model.total_price), 0),
            )
            .where(self.model.created_at.between(start_date, end_date))
            .group_by(self.model.status)
        )
        status_stats = await self.session.execute(query)
        return status_stats.all()

    async def get_daily_income(self, start_date, end_date) -> list[dict[str, Any]]:
        end_date = end_date + timedelta(days=1)
        query = (
            select(
                func.date(self.model.created_at).label(
                    "date"
                ),  # Преобразуем created_at в дату
                func.sum(self.model.total_price).label("amount"),
            )
            .where(
                self.model.created_at.between(start_date, end_date),
                self.model.status.in_([RentalStatus.ACTIVE, RentalStatus.COMPLETED]),
            )
            .group_by(func.date(self.model.created_at))  # Группируем по дате
        ).order_by(
            func.date(self.model.created_at)  # Сортируем по дате
        )

        result = await self.session.execute(query)
        rows = result.mappings().all()
        return [
            {"date": row["date"].strftime("%d-%m-%Y"), "amount": float(row["amount"])}
            for row in rows
        ]

    async def update_expired_rentals_status(self):
        query = (
            update(self.model)
            .where(
                (self.model.status == RentalStatus.ACTIVE)
                & (self.model.end_time < datetime.now())
            )
            .values(status=RentalStatus.COMPLETED)
        )
        await self.session.execute(query)
