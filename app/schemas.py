from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional


class DoctorCreate(BaseModel):
    full_name: str
    email: str
    work_start: time
    work_end: time


class PatientCreate(BaseModel):
    full_name: str
    email: str


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    slot_time: datetime


class AppointmentCancel(BaseModel):
    reason: str


class AppointmentReschedule(BaseModel):
    new_slot_time: datetime
