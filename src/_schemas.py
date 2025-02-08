from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# User схемы
class UserCreate(BaseModel):
    username: str
    phone_number: Optional[str] = None
    is_active: bool = True


class UserRead(BaseModel):
    id: int
    username: str
    phone_number: Optional[str]
    is_active: bool
    registration_date: datetime

    class Config:
        from_attributes = True


# ScooterStatus Enum
class ScooterStatusEnum(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    UNDER_MAINTENANCE = "under_maintenance"


# Scooter схемы
class ScooterCreate(BaseModel):
    model: str
    status: Optional[ScooterStatusEnum] = ScooterStatusEnum.AVAILABLE
    location: Optional[str] = None
    battery_level: Optional[float] = 100.0


class ScooterRead(BaseModel):
    id: int
    model: str
    status: ScooterStatusEnum
    location: Optional[str]
    battery_level: float

    class Config:
        from_attributes = True


# Rental схемы
class RentalCreate(BaseModel):
    user_id: int
    scooter_id: int
    end_time: Optional[datetime] = None
    total_price: Optional[float] = None


class RentalRead(BaseModel):
    id: int
    user_id: int
    scooter_id: int
    end_time: Optional[datetime]
    total_price: Optional[float]

    class Config:
        from_attributes = True


# Payment схемы
class PaymentCreate(BaseModel):
    rental_id: int
    amount: float
    payment_time: Optional[datetime] = None


class PaymentRead(BaseModel):
    id: int
    rental_id: int
    amount: float
    payment_time: datetime

    class Config:
        orm_mode = True


# Location схемы
class LocationCreate(BaseModel):
    scooter_id: int
    latitude: float
    longitude: float


class LocationRead(BaseModel):
    id: int
    scooter_id: int
    latitude: float
    longitude: float

    class Config:
        from_attributes = True
