from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import Form
from pydantic import BaseModel

from schemas import ScooterDisplay


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

