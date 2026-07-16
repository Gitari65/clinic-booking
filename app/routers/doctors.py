from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from ..database import SessionLocal
from .. import crud, models, schemas
from ..utils import generate_slots

router = APIRouter(prefix="/doctors", tags=["Doctors"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_doctor(data: schemas.DoctorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_doctor(db, data)
    except crud.BusinessLogicError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{doctor_id}/availability")
def get_availability(doctor_id: int, query_date: date, db: Session = Depends(get_db)):

    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    slots = generate_slots(doctor, query_date)

    booked = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.cancelled == False
    ).all()

    booked_times = {appt.slot_time for appt in booked}

    available = [slot for slot in slots if slot not in booked_times]

    return {"available_slots": available}