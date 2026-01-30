from pydantic import BaseModel

class DriverRegister(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    license_number: str

class DriverLogin(BaseModel):
    email: str
    password: str

class DriverUpdate(BaseModel):
    name: str | None = None
    vehicle_number: str | None = None
    is_available: bool | None = None

class DriverResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    license_number: str
    vehicle_number: str | None
    is_available: bool
    is_active: bool

    class Config:
        from_attributes = True
