from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

# --------------------- USER ---------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer)
    is_active = Column(Boolean, default=True)

# --------------------- PATIENT ---------------------
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    age = Column(Integer)
    phone = Column(String)
    disease = Column(String)

    # Link to Doctor
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    doctor = relationship("Doctor", back_populates="patients")

# --------------------- DOCTOR ---------------------
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    specialty = Column(String)
    phone = Column(String)

    # Relationship to patients
    patients = relationship("Patient", back_populates="doctor")
