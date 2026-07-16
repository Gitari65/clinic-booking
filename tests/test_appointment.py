import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import models, crud, schemas

# 🔧 Setup test database (in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


# 🧑‍⚕️ Helper: create doctor
def create_test_doctor(db):
    doctor = models.Doctor(
        full_name="Dr Test",
        email="test@example.com",
        work_start=datetime.strptime("09:00", "%H:%M").time(),
        work_end=datetime.strptime("17:00", "%H:%M").time()
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_future_slot(hour: int = 10):
    slot = datetime.utcnow() + timedelta(days=1)
    return slot.replace(hour=hour, minute=0, second=0, microsecond=0)


# ✅ TEST: successful booking
def test_create_appointment_success(db):
    doctor = create_test_doctor(db)

    data = schemas.AppointmentCreate(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=get_future_slot(10)
    )

    appt = crud.create_appointment(db, data)

    assert appt.id is not None
    assert appt.doctor_id == doctor.id


# ✅ TEST: timezone-aware input is accepted
def test_create_appointment_accepts_timezone_aware_datetime(db):
    doctor = create_test_doctor(db)

    slot_time = datetime.now(timezone.utc) + timedelta(days=1, hours=2)
    slot_time = slot_time.replace(minute=0, second=0, microsecond=0)

    data = schemas.AppointmentCreate(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=slot_time
    )

    appt = crud.create_appointment(db, data)

    assert appt.id is not None
    assert appt.doctor_id == doctor.id


# ❌ TEST: cannot book same slot twice
def test_double_booking_fails(db):
    doctor = create_test_doctor(db)

    slot = get_future_slot(10)

    data = schemas.AppointmentCreate(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=slot
    )

    crud.create_appointment(db, data)

    with pytest.raises(Exception):
        crud.create_appointment(db, data)


# ❌ TEST: cannot book past
def test_booking_in_past_fails(db):
    doctor = create_test_doctor(db)

    data = schemas.AppointmentCreate(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=datetime.utcnow() - timedelta(hours=1)
    )

    with pytest.raises(Exception):
        crud.create_appointment(db, data)


# ❌ TEST: cancel appointment
def test_cancel_appointment(db):
    doctor = create_test_doctor(db)

    data = schemas.AppointmentCreate(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=get_future_slot(10)
    )

    appt = crud.create_appointment(db, data)

    cancelled = crud.cancel_appointment(db, appt.id, "Not needed")

    assert cancelled.cancelled is True


# 🔁 TEST: reschedule
def test_reschedule_appointment(db):
    doctor = create_test_doctor(db)

    original_time = get_future_slot(10)
    new_time = get_future_slot(12)

    data = schemas.AppointmentCreate(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=original_time
    )

    appt = crud.create_appointment(db, data)

    updated = crud.reschedule_appointment(db, appt.id, new_time)

    assert updated.slot_time == new_time
