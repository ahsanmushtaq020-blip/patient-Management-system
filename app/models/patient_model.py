from pydantic import BaseModel




class Patient(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    email: str
    phone: str