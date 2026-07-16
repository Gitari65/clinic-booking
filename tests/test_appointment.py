import pytest
from datetime import datetime, timedelta
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


# 🎯 BONUS: upcoming patient appointments are returned in order
def test_patient_upcoming_appointments_are_sorted(db):
    doctor = create_test_doctor(db)

    earlier = datetime.utcnow() + timedelta(days=1, hours=2)
    later = datetime.utcnow() + timedelta(days=1, hours=5)

    first = models.Appointment(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=earlier
    )
    second = models.Appointment(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=later
    )

    db.add_all([first, second])
    db.commit()

    appointments = db.query(models.Appointment).filter(
        models.Appointment.patient_id == 1,
        models.Appointment.cancelled == False
    ).order_by(models.Appointment.slot_time).all()

    assert [appt.slot_time for appt in appointments] == sorted([appt.slot_time for appt in appointments])


# ⏰ BONUS: cannot book within 1 hour of now
def test_booking_within_one_hour_fails(db):
    doctor = create_test_doctor(db)

    data = schemas.AppointmentCreate(
        doctor_id=doctor.id,
        patient_id=1,
        slot_time=datetime.utcnow() + timedelta(minutes=30)
    )

    with pytest.raises(ValueError):
        crud.create_appointment(db, data)


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
