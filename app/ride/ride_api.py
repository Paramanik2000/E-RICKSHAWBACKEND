from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.ride.ride_schema import RideCreate, RideResponse
from app.ride.ride_service import (
    create_ride,
    get_ride_by_id,
    get_rides_by_user,
    get_rides_by_driver,
    start_ride,
    complete_ride,
    cancel_ride
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health():
    return {"ride_service": "OK"}

@router.post("/", response_model=RideResponse)
def book_ride(data: RideCreate, db: Session = Depends(get_db)):
    return create_ride(db, data)

@router.get("/{ride_id}", response_model=RideResponse)
def get_ride(ride_id: int, db: Session = Depends(get_db)):
    return get_ride_by_id(db, ride_id)

@router.get("/user/{user_id}", response_model=list[RideResponse])
def rides_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_rides_by_user(db, user_id)

@router.get("/driver/{driver_id}", response_model=list[RideResponse])
def rides_by_driver(driver_id: int, db: Session = Depends(get_db)):
    return get_rides_by_driver(db, driver_id)

@router.post("/{ride_id}/start", response_model=RideResponse)
def start(ride_id: int, db: Session = Depends(get_db)):
    return start_ride(db, ride_id)

@router.post("/{ride_id}/complete", response_model=RideResponse)
def complete(ride_id: int, db: Session = Depends(get_db)):
    return complete_ride(db, ride_id)

@router.post("/{ride_id}/cancel", response_model=RideResponse)
def cancel(ride_id: int, db: Session = Depends(get_db)):
    return cancel_ride(db, ride_id)
