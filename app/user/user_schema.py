from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str      # plain string
    phone: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str
    is_email_verified: bool
    is_active: bool

    class Config:
        from_attributes = True
