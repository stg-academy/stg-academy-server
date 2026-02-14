from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.user import User
from ..schemas.enroll import EnrollCreate, EnrollUpdate, EnrollResponse, EnrollDetailResponse
from ..crud.enroll import EnrollCRUD
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/enrolls", tags=["enrolls"])

@router.post("/", response_model=EnrollResponse)
async def create_enroll(
    enroll: EnrollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return EnrollCRUD.create_enroll(db, enroll, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[EnrollDetailResponse])
async def get_enrolls(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return EnrollCRUD.get_enrolls_with_details(db, skip=skip, limit=limit)

@router.get("/users/{user_id}/enrolls", response_model=List[EnrollDetailResponse])
async def get_enrolls_by_user(
    user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return EnrollCRUD.get_enrolls_by_user(db, user_id, skip=skip, limit=limit)

@router.get("/sessions/{session_id}/enrolls", response_model=List[EnrollDetailResponse])
async def get_enrolls_by_session(
    session_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return EnrollCRUD.get_enrolls_by_session(db, session_id, skip=skip, limit=limit)

@router.put("/{enroll_id}", response_model=EnrollResponse)
async def update_enroll(
    enroll_id: UUID,
    enroll_update: EnrollUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enroll = EnrollCRUD.update_enroll(db, enroll_id, enroll_update, current_user)
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enroll

@router.get("/users/{user_id}/sessions/{session_id}", response_model=EnrollResponse)
async def get_user_enrollment_in_session(
    user_id: UUID,
    session_id: UUID,
    db: Session = Depends(get_db)
):
    enroll = EnrollCRUD.get_user_enrollment_in_session(db, user_id, session_id)
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enroll