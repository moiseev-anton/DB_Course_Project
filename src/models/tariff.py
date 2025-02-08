from sqlalchemy import Column, Integer, String, Numeric, Interval
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Название тарифа
    price = Column(Numeric(10, 2), nullable=False)  # Цена за единицу времени
    unit = Column(Interval, nullable=False)  # Интервал (например, '1 hour')

    scooters = relationship("Scooter", backref="tariff")  # Связь с самокатами

    @hybrid_property
    def unit_minutes(self):
        return self.unit.total_seconds() // 60
