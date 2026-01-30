from pydantic import BaseModel

class RideCreate(BaseModel):
    user_id: int
    pickup_location: str
    drop_location: str
    distance_km: float

class RideResponse(BaseModel):
    id: int
    user_id: int
    driver_id: int | None
    pickup_location: str
    drop_location: str
    distance_km: float
    fare: float
    status: str

    class Config:
        from_attributes = True
