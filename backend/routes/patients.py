from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Patient, Doctor
from backend.dependencies import require_role

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add patient
@router.post("/add")
def add_patient(data: dict, db: Session = Depends(get_db), user=Depends(require_role([1,2,3]))):
    p = Patient(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"message": "Patient added", "patient": {
        "id": p.id,
        "full_name": p.full_name,
        "age": p.age,
        "phone": p.phone,
        "disease": p.disease,
        "doctor_id": p.doctor_id
    }}

# List patients with doctor names
@router.get("/list")
def list_patients(db: Session = Depends(get_db), user=Depends(require_role([1,2,3]))):
    patients = db.query(Patient).all()
    result = []
    for p in patients:
        doctor = db.query(Doctor).filter(Doctor.id == getattr(p, "doctor_id", None)).first()
        result.append({
            "id": p.id,
            "full_name": p.full_name,
            "age": p.age,
            "phone": p.phone,
            "disease": p.disease,
            "doctor_id": p.doctor_id,
            "doctor_name": doctor.name if doctor else "N/A"
        })
    return result

# Update patient
@router.put("/update/{pid}")
def update_patient(pid: int, updates: dict, db: Session = Depends(get_db), user=Depends(require_role([1,2,3]))):
    p = db.query(Patient).filter(Patient.id == pid).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in updates.items():
        setattr(p, key, value)
    db.commit()
    return {"message": "Patient updated"}

# Delete patient
@router.delete("/delete/{pid}")
def delete_patient(pid: int, db: Session = Depends(get_db), user=Depends(require_role([1,2,3]))):
    p = db.query(Patient).filter(Patient.id == pid).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(p)
    db.commit()
    return {"message": "Patient deleted"}
