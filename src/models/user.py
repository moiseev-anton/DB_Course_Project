import uuid
import enum

from sqlalchemy import Column, String, Boolean, DateTime, text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50))
    surname = Column(String(50))
    phone = Column(String(15), unique=True, nullable=False)
    password_hash = Column(String(256))
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    is_active = Column(Boolean(), default=True, nullable=False)

    rentals = relationship("Rental", backref="user")

