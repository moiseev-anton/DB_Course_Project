from pydantic import BaseModel


class LocationDisplay(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True
