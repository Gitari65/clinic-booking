from sqlalchemy.orm import session
from . import models
from datetime import datetime


def create_appointment(db: session.Session, doctor_id: int, patient_id: int, slot_time: datetime):

    #1 validate not in past
    if slot_time < datetime.now():
        raise ValueError("Cannot book an appointment in the past.")
    
    #2 validate doctor exists
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise ValueError("Doctor not found.")
    
    #3 validate working hours
    if not (doctor.work_start <= slot_time.time() <= doctor.work_end):
        raise ValueError("Appointment time is outside of doctor's working hours.")
    
    #4 Create appointment(DB constarint will handle double booking)

    appointment = models.Appointment(doctor_id=doctor_id, patient_id=patient_id, slot_time=slot_time)
    db.add(appointment)
    try:
        db.commit()
        db.refresh(appointment)
    except Exception as e:
        db.rollback()
        raise ValueError("Slot already booked for this doctor.") from e
    
    return appointment

def cancel_appointment(db: session.Session, appointment_id: int, reason: str):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise ValueError("Appointment not found.")
    
    if appt.status != models.AppointmentStatus.BOOKED:
        raise ValueError("Only booked appointments can be cancelled.")
    
    appt.status = models.AppointmentStatus.CANCELLED
    db.commit()
    db.refresh(appt)
    
    return appt

def reschedule_appointment(db: session.Session, appointment_id: int, new_slot_time: datetime):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise ValueError("Appointment not found.")
    
    if appt.status != models.AppointmentStatus.BOOKED:
        raise ValueError("Only booked appointments can be rescheduled.")
    
    # Validate new slot time
    if new_slot_time < datetime.now():
        raise ValueError("Cannot reschedule to a past time.")
    
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appt.doctor_id).first()
    if not doctor:
        raise ValueError("Doctor not found.")
    
    if not (doctor.work_start <= new_slot_time.time() <= doctor.work_end):
        raise ValueError("New appointment time is outside of doctor's working hours.")
    
    # Update the appointment
    appt.slot_time = new_slot_time
    try:
        db.commit()
        db.refresh(appt)
    except Exception as e:
        db.rollback()
        raise ValueError("New slot unavailable for this doctor.") from e
    
    return appt


    

