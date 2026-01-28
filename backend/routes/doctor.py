from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Doctor, Patient
from backend.dependencies import require_role

router = APIRouter(prefix="/doctors", tags=["Doctors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------- Create Doctor ---------------------
@router.post("/create")
def create_doctor(doctor: dict, db: Session = Depends(get_db), user=Depends(require_role([1]))):
    new_doc = Doctor(**doctor)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {"message": "Doctor created", "doctor": {
        "id": new_doc.id,
        "name": new_doc.name,
        "email": new_doc.email,
        "specialty": new_doc.specialty,
        "phone": new_doc.phone,
        "patients": []
    }}

# --------------------- List Doctors with Patients ---------------------
@router.get("/")
def list_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    result = []
    for doc in doctors:
        result.append({
            "id": doc.id,
            "name": doc.name,
            "email": doc.email,
            "specialty": doc.specialty,
            "phone": doc.phone,
            "patients": [{"id": p.id, "full_name": p.full_name, "age": p.age} for p in doc.patients]
        })
    return result

# --------------------- Update Doctor ---------------------
@router.put("/update/{doctor_id}")
def update_doctor(doctor_id: int, updates: dict, db: Session = Depends(get_db), user=Depends(require_role([1]))):
    doc = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for k, v in updates.items():
        setattr(doc, k, v)
    db.commit()
    db.refresh(doc)
    return {
        "message": "Doctor updated",
        "doctor": {
            "id": doc.id,
            "name": doc.name,
            "email": doc.email,
            "specialty": doc.specialty,
            "phone": doc.phone,
            "patients": [{"id": p.id, "full_name": p.full_name, "age": p.age} for p in doc.patients]
        }
    }

# --------------------- Delete Doctor ---------------------
@router.delete("/delete/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db), user=Depends(require_role([1]))):
    doc = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doc)
    db.commit()
    return {"message": "Doctor deleted"}
