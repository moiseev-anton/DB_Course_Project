from pydantic import BaseModel, Field, field_validator
from datetime import date, timedelta
from typing import Optional, List
from decimal import Decimal


class DateRange(BaseModel):
    start_date: date = Field(..., description="Начало периода")
    end_date: date = Field(..., description="Конец периода")

    @classmethod
    def default(cls) -> "DateRange":
        today = date.today()
        return cls(
            start_date=today - timedelta(days=7), end_date=today  # Последняя неделя
        )


# Отчеты
class RentalReport(BaseModel):
    total_rentals: int
    # active_rentals: Optional[int]
    avg_duration: timedelta
    total_revenue: Decimal
    daily_income: list


# class DailyIncomeReport(BaseModel):


class ScooterUsageReport(BaseModel):
    id: int
    model: str
    total_rentals: int
    total_duration: timedelta
    total_revenue: float
    avg_battery_after: float

    @property
    def total_hours(self):
        return self.total_duration.total_seconds() / 3600


class FinancialReport(BaseModel):
    total_income: Decimal = Decimal("0.0")  # ACTIVE + COMPLETED
    pending_payments: Decimal = Decimal("0.0")  # PENDING
    canceled_rentals: int = 0  # CANCELED (количество)
    total_rentals: int = 0  # Все аренды за период
