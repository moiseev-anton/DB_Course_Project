from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
from schemas import ScooterDisplay
from fastapi import Form
from datetime import timedelta


class RentalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RentalCreate(BaseModel):
    user_id: UUID
    scooter_id: int
    unit_count: int
    total_price: float

    @classmethod
    def as_form(
            cls,
            user_id: UUID = Form(...),
            scooter_id: int = Form(...),
            time_delta: timedelta = Form(),
            total_price: float = Form(...)
    ) -> "RentalCreate":
        return cls(user_id=user_id, scooter_id=scooter_id, time_delta=time_delta, total_price=total_price)


class RentalDisplay(RentalCreate):
    id: int
    scooter: ScooterDisplay
    remaining_time: str

    @field_validator('remaining_time', mode='before')
    def calculate_remaining_time(cls, v, values):
        now = datetime.now(datetime.UTC)
        end_time = values.get('end_time')
        if not end_time:
            return "N/A"
        delta = end_time - now
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60
        return f"{hours} ч {minutes} мин"
