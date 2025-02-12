import enum

from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship

from database import Base


class ScooterStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    RENTED = "RENTED"
    MAINTENANCE = "MAINTENANCE"
    RESERVED = "RESERVED"


class Scooter(Base):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(100), nullable=False)
    serial_number = Column(String(50), nullable=False, unique=True)
    status = Column(Enum(ScooterStatus), default=ScooterStatus.AVAILABLE)
    tariff_id = Column(
        Integer, ForeignKey("tariffs.id", ondelete="SET NULL"), nullable=True
    )
    location_id = Column(
        Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    battery_level = Column(Float, default=100.0)
    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))

    rentals = relationship("Rental", backref="scooter")
