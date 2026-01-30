from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    driver_id = Column(Integer, nullable=True)

    pickup_location = Column(String, nullable=False)
    drop_location = Column(String, nullable=False)

    distance_km = Column(Float, nullable=False)
    fare = Column(Float, nullable=False)

    status = Column(String, default="REQUESTED")
