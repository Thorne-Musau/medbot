from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class Symptom(BaseModel):
    name: str
    severity: Optional[str] = None
    duration: Optional[str] = None

class Diagnosis(BaseModel):
    id: Optional[int] = None
    user_id: int
    conversation_id: Optional[int] = None
    symptoms: List[str]
    predictions: List[Dict[str, float]]
    primary_diagnosis: str
    confidence: float
    created_at: datetime = Field(default_factory=datetime.now)

class DiagnosisCreate(BaseModel):
    symptoms: List[str] = Field(..., min_items=1)
    conversation_id: Optional[int] = None

class DiagnosisResponse(BaseModel):
    id: int
    symptoms: List[str]
    predictions: List[Dict[str, float]]
    primary_diagnosis: str
    confidence: float
    created_at: datetime

    class Config:
        orm_mode = True

class DiagnosisHistory(BaseModel):
    id: int
    user_id: int
    conversation_id: Optional[int]
    symptoms: List[str]
    predictions: List[Dict[str, float]]
    primary_diagnosis: str
    confidence: float
    created_at: datetime

    class Config:
        orm_mode = True 