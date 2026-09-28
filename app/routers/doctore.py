from fastapi import APIRouter, HTTPException, Depends, status
from bson.objectid import ObjectId

from app.models.doctor_model import Doctor
from app.database.mongodb import doctor_collection

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# GET ALL DOCTORS
@router.get("/")
async def get_all_doctors():

    doctors = []

    async for doctor in doctor_collection.find():

        doctor["_id"] = str(doctor["_id"])

        doctors.append(doctor)

    return doctors


# GET DOCTOR BY ID
@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str):

    try:

        doctor = await doctor_collection.find_one(
            {"_id": ObjectId(doctor_id)}
        )

        if not doctor:

            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        doctor["_id"] = str(doctor["_id"])

        return doctor

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid doctor ID"
        )


# CREATE DOCTOR
@router.post("/")
def create_doctor(doctor: Doctor):

    doctor_data = doctor.dict()

    result = doctor_collection.insert_one(doctor_data)

    return {
        "message": "Doctor created successfully",
        "doctor_id": str(result.inserted_id)
    }


# UPDATE DOCTOR
@router.put("/{doctor_id}")
def update_doctor(doctor_id: str, doctor: Doctor):

    try:

        doctor_data = doctor.dict()

        result =  doctor_collection.update_one(
            {"_id": ObjectId(doctor_id)},
            {"$set": doctor_data}
        )

        if result.matched_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        return {
            "message": "Doctor updated successfully"
        }

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid doctor ID"
        )


# DELETE DOCTOR
@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: str):

    try:

        result = doctor_collection.delete_one(
            {"_id": ObjectId(doctor_id)}
        )

        if result.deleted_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        return {
            "message": "Doctor deleted successfully"
        }

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid doctor ID"
        )
    


