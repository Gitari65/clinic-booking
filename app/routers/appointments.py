from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from..dependecies import get_db
from .. import crud, models, schemas

router = APIRouter()

@router.post("/appointments/")
def book_appointment(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_appointment(db, data.doctor_id, data.patient_id, data.slot_time)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.patch("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: str, data: schemas.AppointmentCancel, db: Session = Depends(get_db)):
    try:
        return crud.cancel_appointment(db, appointment_id, data.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
