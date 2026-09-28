from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user_model import User
from app.database.mongodb import user_collection

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import admin_only

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"])

from app.auth.dependencies import (
    admin_only,
    doctor_only,
    patient_only
)

# ---------------- REGISTER ----------------
@router.post("/register")
def register(user: User):

    existing_user = user_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "role": user.role if user.role else "patient"
    }

    result = user_collection.insert_one(user_data)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


# ---------------- LOGIN ----------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db_user = user_collection.find_one({"email": form_data.username})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    role = db_user.get("role", "patient")

    token_data = {
        "sub": db_user["email"],
        "role": role
    }

    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ---------------- ADMIN DASHBOARD ----------------
@router.get("/admin/dashboard")
def admin_dashboard(user = Depends(admin_only)):
    return {"message": "Welcome Admin"}




# DOCTOR ROUTE
@router.get("/doctor/dashboard")
def doctor_dashboard(
    user = Depends(doctor_only)
):

    return {
        "message": "Welcome Doctor"
    }


# PATIENT ROUTE
@router.get("/patient/profile")
def patient_profile(
    user = Depends(patient_only)
):

    return {
        "message": "Welcome Patient"
    }


from app.database.mongodb import (
    user_collection,
    appointment_collection,
    prescription_collection
)


@router.get("/admin/stats")
def admin_stats(
    user = Depends(admin_only)
):

    total_users = user_collection.count_documents({})

    total_doctors = user_collection.count_documents(
        {"role": "doctor"}
    )

    total_patients = user_collection.count_documents(
        {"role": "patient"}
    )

    total_appointments = appointment_collection.count_documents({})

    total_prescriptions = prescription_collection.count_documents({})

    return {

        "total_users": total_users,

        "total_doctors": total_doctors,

        "total_patients": total_patients,

        "total_appointments": total_appointments,

        "total_prescriptions": total_prescriptions
    }