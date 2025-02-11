from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum
from typing import Optional
from schemas.tariff_schema import TariffDisplay
from schemas.location_schema import LocationDisplay


class ScooterStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    RENTED = "RENTED"
    MAINTENANCE = "MAINTENANCE"
    RESERVED = "RESERVED"


class ScooterInfo(BaseModel):
    model: str
    serial_number: str

    class Config:
        from_attributes = True


class ScooterBase(ScooterInfo):
    status: ScooterStatus = ScooterStatus.AVAILABLE
    battery_level: float = Field(..., ge=0, le=100)
    location_id: Optional[int] = None
    tariff_id: Optional[int] = None


class ScooterCreate(ScooterBase):
    pass


class ScooterUpdate(BaseModel):
    model: Optional[str] = Field(None, min_length=2, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=5, max_length=50)
    status: Optional[ScooterStatus] = None
    battery_level: Optional[float] = Field(None, ge=0, le=100)
    location_id: Optional[int] = None
    tariff_id: Optional[int] = None


class ScooterDisplay(ScooterBase):
    id: int
    created_at: datetime
    updated_at: datetime
    location: Optional[LocationDisplay] = None
    tariff: Optional[TariffDisplay] = None
    is_available: bool = Field(default=False, exclude=True)
    battery_status: str = Field(default="unknown", exclude=True)

    @field_validator("is_available", mode="before")
    def set_is_available(cls, v, values):
        return values.get("status") == ScooterStatus.AVAILABLE

    @field_validator("battery_status", mode="before")
    def set_battery_status(cls, v, values):
        battery = values.get("battery_level", 0)
        if battery >= 80:
            return "high"
        elif battery >= 30:
            return "medium"
        else:
            return "low"

    class Config:
        from_attributes = True
