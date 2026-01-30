from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.ride.ride_model import Ride
from app.driver.driver_model import Driver

BASE_FARE = 30
PER_KM_RATE = 10


def calculate_fare(distance_km: float) -> float:
    return BASE_FARE + (distance_km * PER_KM_RATE)


def find_available_driver(db: Session):
    return db.query(Driver).filter(
        Driver.is_available == True,
        Driver.is_active == True
    ).first()


def create_ride(db: Session, data):
    if data.distance_km <= 0:
        raise HTTPException(status_code=400, detail="Invalid distance")

    driver = find_available_driver(db)

    fare = calculate_fare(data.distance_km)

    ride = Ride(
        user_id=data.user_id,
        driver_id=driver.id if driver else None,
        pickup_location=data.pickup_location,
        drop_location=data.drop_location,
        distance_km=data.distance_km,
        fare=fare,
        status="ACCEPTED" if driver else "REQUESTED"
    )

    if driver:
        driver.is_available = False

    db.add(ride)
    db.commit()
    db.refresh(ride)
    return ride


def get_ride_by_id(db: Session, ride_id: int):
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride


def get_rides_by_user(db: Session, user_id: int):
    return db.query(Ride).filter(Ride.user_id == user_id).all()


def get_rides_by_driver(db: Session, driver_id: int):
    return db.query(Ride).filter(Ride.driver_id == driver_id).all()


def start_ride(db: Session, ride_id: int):
    ride = get_ride_by_id(db, ride_id)
    if ride.status != "ACCEPTED":
        raise HTTPException(status_code=400, detail="Ride cannot be started")
    ride.status = "STARTED"
    db.commit()
    return ride


def complete_ride(db: Session, ride_id: int):
    ride = get_ride_by_id(db, ride_id)
    if ride.status != "STARTED":
        raise HTTPException(status_code=400, detail="Ride cannot be completed")

    ride.status = "COMPLETED"

    driver = db.query(Driver).filter(Driver.id == ride.driver_id).first()
    if driver:
        driver.is_available = True

    db.commit()
    return ride


def cancel_ride(db: Session, ride_id: int):
    ride = get_ride_by_id(db, ride_id)

    if ride.status in ["COMPLETED", "CANCELLED"]:
        raise HTTPException(status_code=400, detail="Ride cannot be cancelled")

    ride.status = "CANCELLED"

    driver = db.query(Driver).filter(Driver.id == ride.driver_id).first()
    if driver:
        driver.is_available = True

    db.commit()
    return ride
