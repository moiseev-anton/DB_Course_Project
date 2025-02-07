from sqlalchemy import Column, Integer, DateTime, Numeric, text, ForeignKey

from sqlalchemy.orm import relationship
from database import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    rental_id = Column(Integer, ForeignKey("rentals.id"), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_time = Column(DateTime, server_default=text("TIMEZONE('utc', now())"))

    rental = relationship("Rental", backref="payment", uselist=False)

