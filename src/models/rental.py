from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, text, Enum, Interval

import enum
from database import Base
from sqlalchemy.dialects.postgresql import UUID


class RentalStatus(enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    scooter_id = Column(Integer, ForeignKey("scooters.id", ondelete="SET NULL"), nullable=True)
    duration = Column(Interval, nullable=False)
    end_time = Column(DateTime, nullable=True)
    total_price = Column(Numeric(10, 2), nullable=True)
    status = Column(Enum(RentalStatus), default=RentalStatus.PENDING)
    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
