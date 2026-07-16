from datetime import datetime, timedelta


def generate_slots(doctor, query_date):
    slots = []

    current = datetime.combine(query_date, doctor.work_start)
    end = datetime.combine(query_date, doctor.work_end)

    while current < end:
        slots.append(current)
        current += timedelta(minutes=30)

    return slots