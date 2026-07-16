from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from . import models, schemas


def is_slot_taken(db: Session, doctor_id: int, slot_time: datetime):
    return db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.slot_time == slot_time,
        models.Appointment.cancelled == False
    ).first()


def create_appointment(db: Session, data: schemas.AppointmentCreate):
    if data.slot_time < datetime.utcnow():
        raise ValueError("Cannot book past time")

    if data.slot_time < datetime.utcnow() + timedelta(hours=1):
        raise ValueError("Booking must be at least 1 hour ahead")

    doctor = db.query(models.Doctor).filter(models.Doctor.id == data.doctor_id).first()
    if not doctor:
        raise ValueError("Doctor not found")

    if not (doctor.work_start <= data.slot_time.time() <= doctor.work_end):
        raise ValueError("Outside doctor's working hours")

    if is_slot_taken(db, data.doctor_id, data.slot_time):
        raise ValueError("Slot already taken")

    appointment = models.Appointment(
        doctor_id=data.doctor_id,
        patient_id=data.patient_id,
        slot_time=data.slot_time
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


def cancel_appointment(db: Session, appointment_id: int, reason: str):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise ValueError("Appointment not found")

    if appt.cancelled:
        raise ValueError("Already cancelled")

    appt.cancelled = True
    appt.cancel_reason = reason
    db.commit()
    db.refresh(appt)

    return appt


def reschedule_appointment(db: Session, appointment_id: int, new_slot_time: datetime):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise ValueError("Appointment not found")

    if appt.cancelled:
        raise ValueError("Cannot reschedule cancelled appointment")

    if new_slot_time < datetime.utcnow():
        raise ValueError("Cannot reschedule to a past time")

    doctor = db.query(models.Doctor).filter(models.Doctor.id == appt.doctor_id).first()
    if not doctor:
        raise ValueError("Doctor not found")

    if not (doctor.work_start <= new_slot_time.time() <= doctor.work_end):
        raise ValueError("New appointment time is outside of doctor's working hours")

    if is_slot_taken(db, appt.doctor_id, new_slot_time):
        raise ValueError("New slot already taken")

    appt.slot_time = new_slot_time
    db.commit()
    db.refresh(appt)

    return appt
