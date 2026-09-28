from fastapi import APIRouter, Depends, HTTPException
from bson.objectid import ObjectId

from app.models.apointment_model import Apointment
from app.database.mongodb import appointment_collection
from app.utils.response import (
    success_response,
    error_response
)

from app.utils.response import (
    success_response,
    error_response
)
from app.auth.dependencies import (
    admin_only,
    doctor_only,
    patient_only
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# CREATE APPOINTMENT
@router.post("/")
def create_appointment(
    appointment: Apointment,
    user = Depends(patient_only)
):

    appointment_data = appointment.dict()

    appointment_data["patient_id"] = user["_id"]
    appointment_data["patient_name"] = user["name"]

    result = appointment_collection.insert_one(
        appointment_data
    )

    return success_response(
    "Appointment created successfully",
    {
        "appointment_id": str(result.inserted_id)
    }
)

# GET ALL APPOINTMENTS
@router.get("/")
def get_appointments(
    user = Depends(doctor_only)
):

    appointments = []

    for appointment in appointment_collection.find():

        appointment["_id"] = str(
            appointment["_id"]
        )

        appointments.append(appointment)

    return appointments



@router.get("/my-appointments")
def my_appointments(user = Depends(patient_only)):

    appointments = []

    data = appointment_collection.find(
        {"patient_id": user["_id"]}
    )

    for appointment in data:

        appointment["_id"] = str(appointment["_id"])

        appointments.append(appointment)

    return appointments



@router.get("/doctor-appointments")
def doctor_appointments(user = Depends(doctor_only)):

    appointments = []

    data = appointment_collection.find(
        {"doctor_id": user["_id"]}
    )

    for appointment in data:

        appointment["_id"] = str(appointment["_id"])

        appointments.append(appointment)

    return appointments


@router.get("/search/")
def search_appointments(
    status: str = None,
    date: str = None
):

    query = {}

    if status:
        query["status"] = status

    if date:
        query["date"] = date

    appointments = []

    data = appointment_collection.find(query)

    for appointment in data:

        appointment["_id"] = str(
            appointment["_id"]
        )

        appointments.append(
            appointment
        )

    return appointments


# GET APPOINTMENT BY ID
@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: str,
    user = Depends(doctor_only)
):

    try:

        appointment = appointment_collection.find_one(
            {"_id": ObjectId(appointment_id)}
        )

        if not appointment:

           raise HTTPException(
    status_code=404,
    detail="Appointment not found"
)

        appointment["_id"] = str(
            appointment["_id"]
        )

        return success_response(
         "Appointments fetched successfully",
           appointment
        )


    except:

      error_response(
    404,
    "Appointment not found"
)


# DELETE APPOINTMENT
@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: str,
    user = Depends(admin_only)
):

    try:

        result = appointment_collection.delete_one(
            {"_id": ObjectId(appointment_id)}
        )

        if result.deleted_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        return success_response(
    "Appointment deleted successfully"
)

    except:

        error_response(
    400,
    "Invalid appointment ID"
)



@router.put("/status/{appointment_id}")
def update_status(
    appointment_id: str,
    status: str,
    user = Depends(doctor_only)
):

    appointment = appointment_collection.find_one(
        {"_id": ObjectId(appointment_id)}
    )

    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment["doctor_id"] != user["_id"]:

        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    appointment_collection.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": {"status": status}}
    )

    return success_response(
    "Appointment status updated successfully"
)


# UPDATE APPOINTMENT
@router.put("/{appointment_id}")
def update_appointment(
    appointment_id: str,
    appointment: Apointment,
    user = Depends(admin_only)
):

    try:

        appointment_data = appointment.dict()

        result = appointment_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": appointment_data}
        )

        if result.matched_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        return success_response(
    "Appointment updated successfully"
)   

    except:

        error_response(
    400,
    "Invalid appointment ID"
)
    




