from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from ..models.user import User, Course, Class, Lecture, Attendance, Certification
from ..schemas.user import (
    UserCreate, UserUpdate, CourseCreate, CourseUpdate,
    ClassCreate, ClassUpdate, LectureCreate, LectureUpdate,
    AttendanceCreate, AttendanceUpdate, CertificationCreate, CertificationUpdate
)

class UserCRUD:
    @staticmethod
    def get_user(db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_kakao_id(db: Session, kakao_id: str) -> Optional[User]:
        return db.query(User).filter(User.kakao_id == kakao_id).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            for field, value in user_update.model_dump(exclude_unset=True).items():
                setattr(db_user, field, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> bool:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.is_active = False
            db.commit()
            return True
        return False

class CourseCRUD:
    @staticmethod
    def get_course(db: Session, course_id: UUID) -> Optional[Course]:
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        return db.query(Course).filter(Course.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def create_course(db: Session, course: CourseCreate, user:User) -> Course:
        course_data = course.model_dump()
        course_data['created_by'] = user.id
        course_data['updated_by'] = user.id

        db_course = Course(**course_data)
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course

    @staticmethod
    def update_course(db: Session, course_id: UUID, course_update: CourseUpdate) -> Optional[Course]:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course:
            for field, value in course_update.model_dump(exclude_unset=True).items():
                setattr(db_course, field, value)
            db.commit()
            db.refresh(db_course)
        return db_course

class ClassCRUD:
    @staticmethod
    def get_class(db: Session, class_id: UUID) -> Optional[Class]:
        return db.query(Class).filter(Class.id == class_id).first()

    @staticmethod
    def get_classes_by_course(db: Session, course_id: UUID, skip: int = 0, limit: int = 100) -> List[Class]:
        return db.query(Class).filter(Class.course_id == course_id, Class.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def create_class(db: Session, course_id: UUID, class_data: ClassCreate, user: User) -> Class:
        class_dict = class_data.model_dump()
        class_dict['course_id'] = course_id
        class_dict['created_by'] = user.id
        class_dict['updated_by'] = user.id

        db_class = Class(**class_dict)
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
        return db_class

    @staticmethod
    def update_class(db: Session, class_id: UUID, class_update: ClassUpdate) -> Optional[Class]:
        db_class = db.query(Class).filter(Class.id == class_id).first()
        if db_class:
            for field, value in class_update.model_dump(exclude_unset=True).items():
                setattr(db_class, field, value)
            db.commit()
            db.refresh(db_class)
        return db_class

class LectureCRUD:
    @staticmethod
    def get_lecture(db: Session, lecture_id: UUID) -> Optional[Lecture]:
        return db.query(Lecture).filter(Lecture.id == lecture_id).first()

    @staticmethod
    def get_lectures_by_class(db: Session, class_id: UUID, skip: int = 0, limit: int = 100) -> List[Lecture]:
        return db.query(Lecture).filter(Lecture.class_id == class_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_lecture(db: Session, class_id: UUID, lecture: LectureCreate, user: User) -> Lecture:
        lecture_dict = lecture.model_dump()
        lecture_dict['class_id'] = class_id
        lecture_dict['created_by'] = user.id
        lecture_dict['updated_by'] = user.id

        db_lecture = Lecture(**lecture_dict)
        db.add(db_lecture)
        db.commit()
        db.refresh(db_lecture)
        return db_lecture

    @staticmethod
    def update_lecture(db: Session, lecture_id: UUID, lecture_update: LectureUpdate) -> Optional[Lecture]:
        db_lecture = db.query(Lecture).filter(Lecture.id == lecture_id).first()
        if db_lecture:
            for field, value in lecture_update.model_dump(exclude_unset=True).items():
                setattr(db_lecture, field, value)
            db.commit()
            db.refresh(db_lecture)
        return db_lecture

class AttendanceCRUD:
    @staticmethod
    def get_attendance(db: Session, attendance_id: UUID) -> Optional[Attendance]:
        return db.query(Attendance).filter(Attendance.id == attendance_id).first()

    @staticmethod
    def get_attendances_by_lecture(db: Session, lecture_id: UUID, skip: int = 0, limit: int = 100) -> List[Attendance]:
        return db.query(Attendance).filter(Attendance.lecture_id == lecture_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_attendance(db: Session, lecture_id: UUID, attendance: AttendanceCreate, user: User) -> Attendance:
        attendance_dict = attendance.model_dump()
        attendance_dict['lecture_id'] = lecture_id
        attendance_dict['created_by'] = user.id
        attendance_dict['updated_by'] = user.id

        db_attendance = Attendance(**attendance_dict)
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance

    @staticmethod
    def update_attendance(db: Session, attendance_id: UUID, attendance_update: AttendanceUpdate) -> Optional[Attendance]:
        db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if db_attendance:
            for field, value in attendance_update.model_dump(exclude_unset=True).items():
                setattr(db_attendance, field, value)
            db.commit()
            db.refresh(db_attendance)
        return db_attendance

class CertificationCRUD:
    @staticmethod
    def get_certification(db: Session, certification_id: UUID) -> Optional[Certification]:
        return db.query(Certification).filter(Certification.id == certification_id).first()

    @staticmethod
    def get_certifications(db: Session, skip: int = 0, limit: int = 100) -> List[Certification]:
        return db.query(Certification).offset(skip).limit(limit).all()

    @staticmethod
    def get_certifications_by_user(db: Session, user_id: UUID) -> List[Certification]:
        return db.query(Certification).filter(Certification.user_id == user_id).all()

    @staticmethod
    def create_certification(db: Session, certification: CertificationCreate, user: User) -> Certification:
        certification_dict = certification.model_dump()
        certification_dict['created_by'] = user.id
        certification_dict['updated_by'] = user.id

        db_certification = Certification(**certification_dict)
        db.add(db_certification)
        db.commit()
        db.refresh(db_certification)
        return db_certification