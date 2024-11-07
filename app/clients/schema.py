from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import Optional

class PredictionInput(BaseModel):
    age: int
    gender: str
    # Include all other fields as per your earlier schema

class PredictionOutput(BaseModel):
    prediction: float
    confidence: float
    # Include other relevant fields

    class Config:
        orm_mode = True

class ClientBase(BaseModel):
    age: int
    gender: str
    # Common fields between create and update

class ClientCreate(ClientBase):
    pass  # Additional fields for creation if any

class ClientUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    # Fields that can be updated, all optional

class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True

class PredictionInput(BaseModel):
    age: int
    gender: str
    work_experience: int
    canada_workex: int
    dep_num: int
    canada_born: str
    citizen_status: str
    level_of_schooling: str
    fluent_english: str
    reading_english_scale: int
    speaking_english_scale: int
    writing_english_scale: int
    numeracy_scale: int
    computer_scale: int
    transportation_bool: str
    caregiver_bool: str
    housing: str
    income_source: str
    felony_bool: str
    attending_school: str
    currently_employed: str
    substance_use: str
    time_unemployed: int
    need_mental_health_support_bool: str
