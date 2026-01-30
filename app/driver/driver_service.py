from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.driver.driver_model import Driver
from app.driver.driver_schema import DriverRegister, DriverUpdate
from app.core.security import hash_password, verify_password

def normalize_email(email: str) -> str:
    return email.strip().lower()


def register_driver(db: Session, data: DriverRegister):
    email = normalize_email(data.email)

    if db.query(Driver).filter(Driver.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(Driver).filter(Driver.phone == data.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    if db.query(Driver).filter(Driver.license_number == data.license_number).first():
        raise HTTPException(status_code=400, detail="License already registered")

    driver = Driver(
        name=data.name,
        email=email,
        phone=data.phone,
        password=hash_password(data.password),
        license_number=data.license_number
    )

    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


def authenticate_driver(db: Session, email: str, password: str):
    email = normalize_email(email)

    driver = db.query(Driver).filter(
        Driver.email == email,
        Driver.is_active == True
    ).first()

    if not driver or not verify_password(password, driver.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return driver


def get_all_drivers(db: Session):
    return db.query(Driver).filter(Driver.is_active == True).all()


def get_driver_by_id(db: Session, driver_id: int):
    driver = db.query(Driver).filter(
        Driver.id == driver_id,
        Driver.is_active == True
    ).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver


def update_driver(db: Session, driver_id: int, data: DriverUpdate):
    driver = get_driver_by_id(db, driver_id)

    if data.name is not None:
        driver.name = data.name

    if data.vehicle_number is not None:
        driver.vehicle_number = data.vehicle_number

    if data.is_available is not None:
        driver.is_available = data.is_available

    db.commit()
    db.refresh(driver)
    return driver


def delete_driver(db: Session, driver_id: int):
    driver = get_driver_by_id(db, driver_id)
    driver.is_active = False
    driver.is_available = False
    db.commit()
    return {"message": "Driver deleted"}
