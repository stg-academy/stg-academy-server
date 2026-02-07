from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.user import User
from ..schemas.certification import CertificationCreate, CertificationUpdate, CertificationResponse
from ..crud.certification import CertificationCRUD
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/certifications", tags=["certifications"])

@router.post("", response_model=CertificationResponse)
async def create_certification(
        certification: CertificationCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return CertificationCRUD.create_certification(db, certification, current_user)

@router.get("", response_model=List[CertificationResponse])
async def get_certifications(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return CertificationCRUD.get_certifications(db, skip=skip, limit=limit)

@router.get("/user/{user_id}", response_model=List[CertificationResponse])
async def get_certifications_by_user(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return CertificationCRUD.get_certifications_by_user(db, user_id)

@router.get("/{certification_id}", response_model=CertificationResponse)
async def get_certification(
        certification_id: UUID,
        db: Session = Depends(get_db)
):
    certification = CertificationCRUD.get_certification(db, certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification