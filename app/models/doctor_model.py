from pydantic import BaseModel 

class Doctor(BaseModel):
    id: str
    name: str
    specialty: str
    email: str
    phone: str