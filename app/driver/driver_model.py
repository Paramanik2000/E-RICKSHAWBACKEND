from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)

    password = Column(String, nullable=False)

    license_number = Column(String, unique=True, nullable=False)
    vehicle_number = Column(String, nullable=True)

    is_available = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
