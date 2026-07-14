from sqlite3 import Time

from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Enum,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

import enum 
import uuid
from datetime import datetime

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    work_start=Column(Time, nullable=False)
    work_end=Column(Time, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")

    class Patient(Base):
        __tablename__ = "patients"
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index=True)
        full_name = Column(String, nullable=False)
        email = Column(String, unique=True, nullable=False)

        appointments = relationship("Appointment", back_populates="patient")

    class AppointmentStatus(str, enum.Enum):
        BOOKED = "booked"
        CANCELLED = "cancelled"
        COMPLETED = "completed"
   

    class Appointment(Base):
        __tablename__ = "appointments"
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index=True)
        doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False)
        patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
        slot_time = Column(DateTime, nullable=False)
        status = Column(Enum(AppointmentStatus), default=AppointmentStatus.BOOKED, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow)

        __table_args__ = (
            UniqueConstraint('doctor_id', 'slot_time', name='unique_doctor_slot'),
        )



