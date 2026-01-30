from pydantic import BaseModel

class VehicleCreate(BaseModel):
    number_plate: str
