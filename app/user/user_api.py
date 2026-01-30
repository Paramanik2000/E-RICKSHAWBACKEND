from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jose import jwt

from app.core.database import SessionLocal
from app.core.config import SECRET_KEY, ALGORITHM
from app.user.user_schema import (
    UserRegister,
    UserLogin,
    UserUpdate,
    UserResponse
)
from app.user.user_service import (
    register_user,
    authenticate_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user,
    verify_email
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(user_id: int):
    payload = {"user_id": user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.get("/health")
def health():
    return {"user_service": "OK"}

@router.post("/register", response_model=UserResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, data)

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/{user_id}/verify-email")
def email_verify(user_id: int, db: Session = Depends(get_db)):
    return verify_email(db, user_id)

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, data)

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
