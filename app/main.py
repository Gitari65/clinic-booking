from fastapi import FastAPI
from .database import Base, engine
from .routers import appointments, doctors

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Clinic Booking API is running", "docs": "/docs"}

app.include_router(appointments.router)
app.include_router(doctors.router)