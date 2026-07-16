from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime

from .database import Base, engine, SessionLocal
from .routers import appointments, doctors, patients
from . import models

Base.metadata.create_all(bind=engine)


def seed_sample_doctors():
    db = SessionLocal()
    try:
        doctor_ids = [1, 2, 3, 4, 5]
        for doctor_id in doctor_ids:
            existing = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
            if existing:
                continue

            doctor_names = [
                "Dr. Alice Johnson",
                "Dr. Brian Smith",
                "Dr. Clara Ahmed",
                "Dr. Daniel Kim",
                "Dr. Eva Martinez",
            ]
            emails = [
                "alice@example.com",
                "brian@example.com",
                "clara@example.com",
                "daniel@example.com",
                "eva@example.com",
            ]
            db.add(models.Doctor(
                id=doctor_id,
                full_name=doctor_names[doctor_id - 1],
                email=emails[doctor_id - 1],
                work_start=datetime.strptime("09:00", "%H:%M").time(),
                work_end=datetime.strptime("17:00", "%H:%M").time(),
            ))

        patient_ids = [1, 2, 3, 4, 5]
        for patient_id in patient_ids:
            existing = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
            if existing:
                continue

            patient_names = [
                "Alice Patel",
                "Brian Chen",
                "Clara Gomez",
                "Daniel Brooks",
                "Eva Thompson",
            ]
            emails = [
                "alice.patient@example.com",
                "brian.patient@example.com",
                "clara.patient@example.com",
                "daniel.patient@example.com",
                "eva.patient@example.com",
            ]
            db.add(models.Patient(
                id=patient_id,
                full_name=patient_names[patient_id - 1],
                email=emails[patient_id - 1],
            ))

        db.commit()
    finally:
        db.close()


seed_sample_doctors()

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.get("/")
def read_root():
    return {"message": "Clinic Booking API is running", "docs": "/docs"}

app.include_router(appointments.router)
app.include_router(doctors.router)
app.include_router(patients.router)