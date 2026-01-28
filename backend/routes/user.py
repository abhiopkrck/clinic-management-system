from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User
from backend.security.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_user(data: dict, db: Session = Depends(get_db)):
    user = User(
        full_name=data["full_name"],
        email=data["email"],
        password_hash=hash_password(data["password"]),
        role_id=data["role_id"]
    )
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}
