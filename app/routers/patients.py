from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas, models

router = APIRouter(prefix="/patients", tags=["Patients"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_patient(data: schemas.PatientCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_patient(db, data)
    except crud.BusinessLogicError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
