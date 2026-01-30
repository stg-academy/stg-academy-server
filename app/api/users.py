from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.user import User
from ..schemas.user import (
    UserResponse, UserUpdate,
    CourseResponse, CourseCreate, CourseUpdate,
    ClassResponse, ClassCreate, ClassUpdate,
    LectureResponse, LectureCreate, LectureUpdate,
    AttendanceResponse, AttendanceCreate, AttendanceUpdate,
    CertificationResponse, CertificationCreate, CertificationUpdate
)
from ..crud.user import UserCRUD, CourseCRUD, ClassCRUD, LectureCRUD, AttendanceCRUD, CertificationCRUD
from .auth import get_current_user

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/users", response_model=List[UserResponse])
async def get_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    users = UserCRUD.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    user = UserCRUD.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: UUID,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    user = UserCRUD.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
async def delete_user(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    success = UserCRUD.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated successfully"}


@router.post("/courses", response_model=CourseResponse)
async def create_course(
        course: CourseCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return CourseCRUD.create_course(db, course, current_user)


@router.get("/courses", response_model=List[CourseResponse])
async def get_courses(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return CourseCRUD.get_courses(db, skip=skip, limit=limit)


@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(
        course_id: UUID,
        db: Session = Depends(get_db)
):
    course = CourseCRUD.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(
        course_id: UUID,
        course_update: CourseUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    course = CourseCRUD.update_course(db, course_id, course_update)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/courses/{course_id}/classes", response_model=ClassResponse)
async def create_class(
        course_id: UUID,
        class_data: ClassCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return ClassCRUD.create_class(db, course_id, class_data, current_user)


@router.get("/courses/{course_id}/classes", response_model=List[ClassResponse])
async def get_classes_by_course(
        course_id: UUID,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return ClassCRUD.get_classes_by_course(db, course_id, skip=skip, limit=limit)


@router.get("/classes/{class_id}", response_model=ClassResponse)
async def get_class(
        class_id: UUID,
        db: Session = Depends(get_db)
):
    class_obj = ClassCRUD.get_class(db, class_id)
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj


@router.put("/classes/{class_id}", response_model=ClassResponse)
async def update_class(
        class_id: UUID,
        class_update: ClassUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    class_obj = ClassCRUD.update_class(db, class_id, class_update)
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj


@router.post("/classes/{class_id}/lectures", response_model=LectureResponse)
async def create_lecture(
        class_id: UUID,
        lecture: LectureCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return LectureCRUD.create_lecture(db, class_id, lecture, current_user)


@router.get("/classes/{class_id}/lectures", response_model=List[LectureResponse])
async def get_lectures_by_class(
        class_id: UUID,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return LectureCRUD.get_lectures_by_class(db, class_id, skip=skip, limit=limit)


@router.get("/lectures/{lecture_id}", response_model=LectureResponse)
async def get_lecture(
        lecture_id: UUID,
        db: Session = Depends(get_db)
):
    lecture = LectureCRUD.get_lecture(db, lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture


@router.put("/lectures/{lecture_id}", response_model=LectureResponse)
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


@router.get("/attendances/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance(
        attendance_id: UUID,
        db: Session = Depends(get_db)
):
    attendance = AttendanceCRUD.get_attendance(db, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance


@router.put("/attendances/{attendance_id}", response_model=AttendanceResponse)
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


@router.post("/certifications", response_model=CertificationResponse)
async def create_certification(
        certification: CertificationCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return CertificationCRUD.create_certification(db, certification, current_user)


@router.get("/certifications", response_model=List[CertificationResponse])
async def get_certifications(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return CertificationCRUD.get_certifications(db, skip=skip, limit=limit)


@router.get("/certifications/{certification_id}", response_model=CertificationResponse)
async def get_certification(
        certification_id: UUID,
        db: Session = Depends(get_db)
):
    certification = CertificationCRUD.get_certification(db, certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification


@router.get("/users/{user_id}/certifications", response_model=List[CertificationResponse])
async def get_user_certifications(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return CertificationCRUD.get_certifications_by_user(db, user_id)
