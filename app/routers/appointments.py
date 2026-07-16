from fastapi import APIRouter, Depends, HTTPException
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


def _raise_business_error(exc: ValueError):
    raise HTTPException(status_code=400, detail=str(exc)) from exc


# ✅ BOOK APPOINTMENT
@router.post("/")
def book_appointment(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_appointment(db, data)
    except ValueError as exc:
        _raise_business_error(exc)


# ❌ CANCEL APPOINTMENT
@router.patch("/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int, data: schemas.AppointmentCancel, db: Session = Depends(get_db)):
    try:
        return crud.cancel_appointment(db, appointment_id, data.reason)
    except ValueError as exc:
        _raise_business_error(exc)


# 🔁 RESCHEDULE APPOINTMENT
@router.patch("/{appointment_id}/reschedule")
def reschedule_appointment(appointment_id: int, data: schemas.AppointmentReschedule, db: Session = Depends(get_db)):
    try:
        return crud.reschedule_appointment(db, appointment_id, data.new_slot_time)
    except ValueError as exc:
        _raise_business_error(exc)


# 🎯 BONUS: GET PATIENT APPOINTMENTS
@router.get("/patients/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):

    appointments = db.query(models.Appointment).filter(
        models.Appointment.patient_id == patient_id,
        models.Appointment.cancelled == False
    ).order_by(models.Appointment.slot_time).all()

    return {"appointments": appointments}