from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.user import User
from ..schemas.course import CourseCreate, CourseUpdate, CourseResponse
from ..crud.course import CourseCRUD
from .auth import get_current_user

router = APIRouter(prefix="/api/courses", tags=["courses"])

@router.post("", response_model=CourseResponse)
async def create_course(
        course: CourseCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return CourseCRUD.create_course(db, course, current_user)

@router.get("", response_model=List[CourseResponse])
async def get_courses(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return CourseCRUD.get_courses(db, skip=skip, limit=limit)

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
        course_id: UUID,
        db: Session = Depends(get_db)
):
    course = CourseCRUD.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
        course_id: UUID,
        course_update: CourseUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    course = CourseCRUD.update_course(db, course_id, course_update, current_user)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course