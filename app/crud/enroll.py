from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from ..models.user import Enroll, User, Session as SessionModel, Course
from ..schemas.enroll import EnrollCreate, EnrollUpdate, EnrollDetailResponse

class EnrollCRUD:
    @staticmethod
    def get_enroll(db: Session, enroll_id: UUID) -> Optional[Enroll]:
        return db.query(Enroll).filter(Enroll.id == enroll_id).first()

    @staticmethod
    def get_enrolls(db: Session, skip: int = 0, limit: int = 100) -> List[Enroll]:
        return db.query(Enroll).order_by(Enroll.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_enrolls_with_details(db: Session, skip: int = 0, limit: int = 100) -> List[EnrollDetailResponse]:
        """Get enrollments with user_name, auth_type, session_title, and course_name"""
        results = (
            db.query(
                Enroll,
                User.username.label('user_name'),
                User.auth_type.label('auth_type'),
                SessionModel.title.label('session_title'),
                Course.title.label('course_name')
            )
            .join(User, Enroll.user_id == User.id)
            .join(SessionModel, Enroll.session_id == SessionModel.id)
            .join(Course, SessionModel.course_id == Course.id)
            .order_by(Enroll.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        response_list = []
        for enroll, user_name, auth_type, session_title, course_name in results:
            response_data = {
                "id": enroll.id,
                "user_id": enroll.user_id,
                "session_id": enroll.session_id,
                "enroll_status": enroll.enroll_status,
                "user_name": user_name,
                "auth_type": auth_type,
                "session_title": session_title,
                "course_name": course_name,
                "created_at": enroll.created_at,
                "updated_at": enroll.updated_at,
                "created_by": enroll.created_by,
                "updated_by": enroll.updated_by
            }
            response_list.append(EnrollDetailResponse(**response_data))

        return response_list

    @staticmethod
    def get_enrolls_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[EnrollDetailResponse]:
        """Get enrollments by user with session and course details"""
        results = (
            db.query(
                Enroll,
                User.username.label('user_name'),
                User.auth_type.label('auth_type'),
                SessionModel.title.label('session_title'),
                Course.title.label('course_name')
            )
            .join(User, Enroll.user_id == User.id)
            .join(SessionModel, Enroll.session_id == SessionModel.id)
            .join(Course, SessionModel.course_id == Course.id)
            .filter(Enroll.user_id == user_id)
            .order_by(Enroll.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        response_list = []
        for enroll, user_name, auth_type, session_title, course_name in results:
            response_data = {
                "id": enroll.id,
                "user_id": enroll.user_id,
                "session_id": enroll.session_id,
                "enroll_status": enroll.enroll_status,
                "user_name": user_name,
                "auth_type": auth_type,
                "session_title": session_title,
                "course_name": course_name,
                "created_at": enroll.created_at,
                "updated_at": enroll.updated_at,
                "created_by": enroll.created_by,
                "updated_by": enroll.updated_by
            }
            response_list.append(EnrollDetailResponse(**response_data))

        return response_list

    @staticmethod
    def get_enrolls_by_session(db: Session, session_id: UUID, skip: int = 0, limit: int = 100) -> List[EnrollDetailResponse]:
        """Get enrollments by session with user and course details"""
        results = (
            db.query(
                Enroll,
                User.username.label('user_name'),
                User.auth_type.label('auth_type'),
                SessionModel.title.label('session_title'),
                Course.title.label('course_name')
            )
            .join(User, Enroll.user_id == User.id)
            .join(SessionModel, Enroll.session_id == SessionModel.id)
            .join(Course, SessionModel.course_id == Course.id)
            .filter(Enroll.session_id == session_id)
            .order_by(Enroll.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        response_list = []
        for enroll, user_name, auth_type, session_title, course_name in results:
            response_data = {
                "id": enroll.id,
                "user_id": enroll.user_id,
                "session_id": enroll.session_id,
                "enroll_status": enroll.enroll_status,
                "user_name": user_name,
                "auth_type": auth_type,
                "session_title": session_title,
                "course_name": course_name,
                "created_at": enroll.created_at,
                "updated_at": enroll.updated_at,
                "created_by": enroll.created_by,
                "updated_by": enroll.updated_by
            }
            response_list.append(EnrollDetailResponse(**response_data))

        return response_list

    @staticmethod
    def create_enroll(db: Session, enroll: EnrollCreate, user: User) -> Enroll:
        # Check if user is already enrolled in this session
        existing_enroll = db.query(Enroll).filter(
            Enroll.user_id == enroll.user_id,
            Enroll.session_id == enroll.session_id
        ).first()

        if existing_enroll:
            raise ValueError("User is already enrolled in this session")

        enroll_dict = enroll.model_dump()
        enroll_dict['created_by'] = user.id
        enroll_dict['updated_by'] = user.id

        db_enroll = Enroll(**enroll_dict)
        db.add(db_enroll)
        db.commit()
        db.refresh(db_enroll)
        return db_enroll


    @staticmethod
    def update_enroll(db: Session, enroll_id: UUID, enroll_update: EnrollUpdate, user: User) -> Optional[Enroll]:
        """Update enrollment status"""
        enroll_dict = enroll_update.model_dump(exclude_unset=True)
        enroll_dict['updated_by'] = user.id

        db_enroll = db.query(Enroll).filter(Enroll.id == enroll_id).first()
        if db_enroll:
            for field, value in enroll_dict.items():
                setattr(db_enroll, field, value)
            db.commit()
            db.refresh(db_enroll)
        return db_enroll

    @staticmethod
    def get_user_enrollment_in_session(db: Session, user_id: UUID, session_id: UUID) -> Optional[Enroll]:
        """Check if a specific user is enrolled in a specific session"""
        return db.query(Enroll).filter(
            Enroll.user_id == user_id,
            Enroll.session_id == session_id
        ).first()