from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.user import User
from ..schemas.lecture import LectureCreate, LectureUpdate, LectureResponse
from ..crud.lecture import LectureCRUD
from .auth import get_current_user

router = APIRouter(prefix="/api/lectures", tags=["lectures"])

@router.post("", response_model=LectureResponse)
async def create_lecture(
        lecture: LectureCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return LectureCRUD.create_lecture(db, lecture, current_user)

@router.get("", response_model=List[LectureResponse])
async def get_lectures(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return LectureCRUD.get_lectures(db, skip=skip, limit=limit)

@router.get("/session/{session_id}", response_model=List[LectureResponse])
async def get_lectures_by_session(
        session_id: UUID,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return LectureCRUD.get_lectures_by_session(db, session_id, skip=skip, limit=limit)

@router.get("/{lecture_id}", response_model=LectureResponse)
async def get_lecture(
        lecture_id: UUID,
        db: Session = Depends(get_db)
):
    lecture = LectureCRUD.get_lecture(db, lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture

@router.put("/{lecture_id}", response_model=LectureResponse)
async def update_lecture(
        lecture_id: UUID,
        lecture_update: LectureUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    lecture = LectureCRUD.update_lecture(db, lecture_id, lecture_update)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture

@router.delete("/{lecture_id}")
async def delete_lecture(
        lecture_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    success = LectureCRUD.delete_lecture(db, lecture_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return {"message": "Lecture deactivated successfully"}