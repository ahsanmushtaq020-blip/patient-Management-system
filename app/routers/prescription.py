from fastapi import APIRouter, Depends
from app.models.prescription_model import Prescription
from app.database.mongodb import prescription_collection

from app.auth.dependencies import doctor_only


router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


@router.post("/")
def create_prescription(
    prescription: Prescription,
    user = Depends(doctor_only)
):

    prescription_data = prescription.dict()

    result = prescription_collection.insert_one(
        prescription_data
    )

    return {
        "message": "Prescription created",
        "id": str(result.inserted_id)
    }

from app.auth.dependencies import patient_only


@router.get("/my-prescriptions")
def my_prescriptions(
    user = Depends(patient_only)
):

    prescriptions = []

    data = prescription_collection.find(
        {"patient_id": user["_id"]}
    )

    for prescription in data:

        prescription["_id"] = str(
            prescription["_id"]
        )

        prescriptions.append(
            prescription
        )

    return prescriptions