from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.user import User
from ..schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from ..crud.attendance import AttendanceCRUD
from .auth import get_current_user

router = APIRouter(prefix="/api/attendances", tags=["attendances"])

@router.post("/lectures/{lecture_id}/attendances", response_model=AttendanceResponse)
async def create_attendance(
        lecture_id: UUID,
        attendance: AttendanceCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return AttendanceCRUD.create_attendance(db, lecture_id, attendance, current_user)

@router.get("/lectures/{lecture_id}/attendances", response_model=List[AttendanceResponse])
async def get_attendances_by_lecture(
        lecture_id: UUID,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return AttendanceCRUD.get_attendances_by_lecture(db, lecture_id, skip=skip, limit=limit)

@router.get("/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance(
        attendance_id: UUID,
        db: Session = Depends(get_db)
):
    attendance = AttendanceCRUD.get_attendance(db, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
        attendance_id: UUID,
        attendance_update: AttendanceUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    attendance = AttendanceCRUD.update_attendance(db, attendance_id, attendance_update)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance