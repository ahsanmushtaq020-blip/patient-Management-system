from fastapi import APIRouter, Depends, HTTPException
from bson.objectid import ObjectId

from app.models.patient_model import Patient
from app.database.mongodb import patient_collection
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# GET ALL PATIENTS
@router.get("/")
def get_patients():

    patients = []

    for patient in patient_collection.find():

        patient["_id"] = str(patient["_id"])

        patients.append(patient)

    return patients


# CREATE PATIENT
@router.post("/")
def create_patient(patient: Patient):

    patient_data = patient.dict()

    result = patient_collection.insert_one(patient_data)

    return {
        "message": "Patient created successfully",
        "patient_id": str(result.inserted_id)
    }


# GET SINGLE PATIENT
@router.get("/{patient_id}")
def get_patient(patient_id: str):

    try:

        patient = patient_collection.find_one(
            {"_id": ObjectId(patient_id)}
        )

        if patient:

            patient["_id"] = str(patient["_id"])

            return patient

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid patient ID"
        )


# UPDATE PATIENT
@router.put("/{patient_id}")
def update_patient(patient_id: str, patient: Patient):

    try:

        patient_data = patient.dict()

        result = patient_collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": patient_data}
        )

        if result.matched_count > 0:

            return {
                "message": "Patient updated successfully"
            }

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid patient ID"
        )


# DELETE PATIENT
@router.delete("/{patient_id}")
def delete_patient(patient_id: str):

    try:

        result = patient_collection.delete_one(
            {"_id": ObjectId(patient_id)}
        )

        if result.deleted_count > 0:

            return {
                "message": "Patient deleted successfully"
            }

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid patient ID"
        )
    


@router.get("/profile")
async def profile(
    current_user = Depends(get_current_user)
):

    return {
        "message": "Protected Route",
        "user": current_user
    }

@router.get("/me")
def get_my_profile(current_user = Depends(get_current_user)):
    return current_user



