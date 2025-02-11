from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from fastapi import Form
from pydantic import BaseModel, field_validator
from models import Scooter

from schemas import ScooterInfo


class RentalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RentalCreate(BaseModel):
    unit_count: int

    @classmethod
    def as_form(cls, unit_count: int = Form(..., gt=0)) -> "RentalCreate":
        return cls(unit_count=unit_count)


class RentalDisplay(BaseModel):
    id: int
    status: str
    scooter_model: str
    scooter_battery_level: float
    end_time: Optional[datetime] = None
    duration: Optional[int] = None  # В минутах
    total_price: float
    remaining_time: Optional[int] = None  # В секундах если аренда активна)


class RentalInfoDisplay(BaseModel):
    id: int
    status: str
    duration: timedelta
    total_price: float
    end_time: Optional[datetime] = None
    scooter: ScooterInfo

    @property
    def duration_str(self) -> str:
        hours, remainder = divmod(self.duration.seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02}:{minutes:02}"

    @field_validator("scooter", mode="before")
    def validate_scooter(cls, value):
        if isinstance(value, Scooter):  # Если это модель SQLAlchemy
            return ScooterInfo(model=value.model, serial_number=value.serial_number)
        return value

    class Config:
        from_attributes = True
