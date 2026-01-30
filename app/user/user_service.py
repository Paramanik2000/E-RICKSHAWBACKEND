from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.user.user_model import User
from app.user.user_schema import UserRegister, UserUpdate
from app.core.security import hash_password, verify_password

def normalize_email(email: str) -> str:
    return email.strip().lower()

def register_user(db: Session, data: UserRegister):
    email = normalize_email(data.email)

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.phone == data.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    user = User(
        name=data.name,
        email=email,
        phone=data.phone,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    email = normalize_email(email)

    user = db.query(User).filter(
        User.email == email,
        User.is_active == True
    ).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


def get_users(db: Session):
    return db.query(User).filter(User.is_active == True).all()


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = get_user_by_id(db, user_id)

    if data.name:
        user.name = data.name

    db.commit()
    db.refresh(user)
    return user


def verify_email(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    user.is_email_verified = True
    db.commit()
    return {"message": "Email verified"}


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()
    return {"message": "User deleted"}
