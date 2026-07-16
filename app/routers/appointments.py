from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas, models

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ BOOK APPOINTMENT
@router.post("/")
def book_appointment(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, data)


# ❌ CANCEL APPOINTMENT
@router.patch("/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int, data: schemas.AppointmentCancel, db: Session = Depends(get_db)):
    return crud.cancel_appointment(db, appointment_id, data.reason)


# 🔁 RESCHEDULE APPOINTMENT
@router.patch("/{appointment_id}/reschedule")
def reschedule_appointment(appointment_id: int, data: schemas.AppointmentReschedule, db: Session = Depends(get_db)):
    return crud.reschedule_appointment(db, appointment_id, data.new_slot_time)


# 🎯 BONUS: GET PATIENT APPOINTMENTS
@router.get("/patients/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):

    appointments = db.query(models.Appointment).filter(
        models.Appointment.patient_id == patient_id,
        models.Appointment.cancelled == False
    ).order_by(models.Appointment.slot_time).all()

    return {"appointments": appointments}