from pydantic import BaseModel


class Prescription(BaseModel):

    patient_id: str
    doctor_id: str
    medicine: str
    dosage: str
    instructions: str