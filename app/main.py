from fastapi import FastAPI

from app.routers.patient import router as patient_router
from app.routers.doctore import router as doctor_router
from app.routers.apointment import router as appointment_router
from app.routers.auth import router as auth_router
from app.routers.prescription import router as prescription_router

app = FastAPI()

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(auth_router)
app.include_router(prescription_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Patient Management System API"}