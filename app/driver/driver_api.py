from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jose import jwt

from app.core.database import SessionLocal
from app.core.config import SECRET_KEY, ALGORITHM
from app.driver.driver_schema import (
    DriverRegister,
    DriverLogin,
    DriverUpdate,
    DriverResponse
)
from app.driver.driver_service import (
    register_driver,
    authenticate_driver,
    get_all_drivers,
    get_driver_by_id,
    update_driver,
    delete_driver
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(driver_id: int):
    payload = {"driver_id": driver_id}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.get("/health")
def health():
    return {"driver_service": "OK"}

@router.post("/register", response_model=DriverResponse)
def register(data: DriverRegister, db: Session = Depends(get_db)):
    return register_driver(db, data)

@router.post("/login")
def login(data: DriverLogin, db: Session = Depends(get_db)):
    driver = authenticate_driver(db, data.email, data.password)
    token = create_token(driver.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/", response_model=list[DriverResponse])
def list_drivers(db: Session = Depends(get_db)):
    return get_all_drivers(db)

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    return get_driver_by_id(db, driver_id)

@router.put("/{driver_id}", response_model=DriverResponse)
def update(driver_id: int, data: DriverUpdate, db: Session = Depends(get_db)):
    return update_driver(db, driver_id, data)

@router.delete("/{driver_id}")
def delete(driver_id: int, db: Session = Depends(get_db)):
    return delete_driver(db, driver_id)
