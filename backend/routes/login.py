from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User
from backend.security.security import verify_password
from backend.security.auth import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data["email"], User.is_active == True).first()

    if not user or not verify_password(data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "role_id": user.role_id
    })

    return {"access_token": token, "token_type": "bearer"}