from pydantic import BaseModel, Field
from datetime import date, time
from typing import Literal


class Apointment(BaseModel):

    patient_id: str = Field(..., min_length=1)
    doctor_id: str = Field(..., min_length=1)

    doctor_name: str
    patient_name: str

    date: date
    time: str

    status: Literal["pending", "approved", "rejected", "completed"] = "pending"
    