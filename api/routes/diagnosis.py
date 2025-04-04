from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.diagnosis_models import (
    DiagnosisCreate,
    DiagnosisResponse,
    DiagnosisHistory
)
from ..models.db_models import Diagnosis as DBDiagnosis
from ..auth.utils import get_current_active_user
from ..models.db_models import User
from ..ml.inference import get_predictor

router = APIRouter()

@router.post("/diagnose", response_model=DiagnosisResponse)
async def create_diagnosis(
    diagnosis: DiagnosisCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        # Get predictions from ML model
        predictor = get_predictor()
        predictions, primary_diagnosis, confidence = predictor.predict(diagnosis.symptoms)

        # Create diagnosis record
        db_diagnosis = DBDiagnosis(
            user_id=current_user.id,
            conversation_id=diagnosis.conversation_id,
            symptoms=diagnosis.symptoms,
            predictions=predictions,
            primary_diagnosis=primary_diagnosis,
            confidence=confidence
        )
        db.add(db_diagnosis)
        db.commit()
        db.refresh(db_diagnosis)
        return db_diagnosis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error making diagnosis: {str(e)}"
        )

@router.get("/diagnoses", response_model=List[DiagnosisHistory])
async def get_diagnosis_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    diagnoses = db.query(DBDiagnosis).filter(
        DBDiagnosis.user_id == current_user.id
    ).all()
    return diagnoses

@router.get("/diagnoses/{diagnosis_id}", response_model=DiagnosisResponse)
async def get_diagnosis(
    diagnosis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    diagnosis = db.query(DBDiagnosis).filter(
        DBDiagnosis.id == diagnosis_id,
        DBDiagnosis.user_id == current_user.id
    ).first()
    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis not found"
        )
    return diagnosis 