from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional

class AppointmentCreate(BaseModel):
    doctor_id: str
    patient_id: str
    slot_time: datetime

class AppointmentCancel(BaseModel):
        reason: str

class AppointmentReschedule(BaseModel):
            new_slot_time: datetime 
            

