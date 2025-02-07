from pydantic import BaseModel
from datetime import timedelta
from typing import Optional


class TariffDisplay(BaseModel):
    id: int
    name: str
    price: float
    unit: timedelta
    description: Optional[str] = None

    class Config:
        from_attributes = True
