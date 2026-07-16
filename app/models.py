from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.types import Time
from sqlalchemy.orm import relationship
from .database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    work_start = Column(Time, nullable=False)
    work_end = Column(Time, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, nullable=False)
    slot_time = Column(DateTime, nullable=False)
    cancelled = Column(Boolean, default=False)
    cancel_reason = Column(String, nullable=True)

    doctor = relationship("Doctor", back_populates="appointments")