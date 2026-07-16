from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    slot_time: datetime


class AppointmentCancel(BaseModel):
    reason: str


class AppointmentReschedule(BaseModel):
    new_slot_time: datetime
