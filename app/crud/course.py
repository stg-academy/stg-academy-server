from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from ..models.user import Course, User
from ..schemas.course import CourseCreate, CourseUpdate

class CourseCRUD:
    @staticmethod
    def get_course(db: Session, course_id: UUID) -> Optional[Course]:
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        return db.query(Course).filter(Course.is_active == True).order_by(Course.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_course(db: Session, course: CourseCreate, user: User) -> Course:
        course_data = course.model_dump()
        course_data['created_by'] = user.id
        course_data['updated_by'] = user.id

        db_course = Course(**course_data)
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course

    @staticmethod
    def update_course(db: Session, course_id: UUID, course_update: CourseUpdate, user: User) -> Optional[Course]:
        course_update_data = course_update.model_dump(exclude_unset=True)
        course_update_data['updated_by'] = user.id

        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course:
            for field, value in course_update_data.items():
                setattr(db_course, field, value)
            db.commit()
            db.refresh(db_course)
        return db_course