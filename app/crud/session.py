from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.user import Course, Lecture
from ..models.user import Session, User
from ..schemas.session import SessionCreate, SessionUpdate, SessionDetailResponse


def calculate_course_status(begin_date: Optional[datetime], end_date: Optional[datetime]) -> str:
    """Calculate course status based on begin_date and end_date"""
    now = datetime.now(timezone.utc)

    # If no dates set, default to NOT_STARTED
    if begin_date is None and end_date is None:
        return "NOT_STARTED"

    # If only begin_date is set
    if begin_date is not None and end_date is None:
        if now < begin_date:
            return "NOT_STARTED"
        else:
            return "IN_PROGRESS"

    # If only end_date is set
    if begin_date is None and end_date is not None:
        if now > end_date:
            return "FINISHED"
        else:
            return "IN_PROGRESS"

    # Both dates set
    if now < begin_date:
        return "NOT_STARTED"
    elif begin_date <= now <= end_date:
        return "IN_PROGRESS"
    else:
        return "FINISHED"


class SessionCRUD:
    @staticmethod
    def get_session(db: Session, session_id: UUID) -> Optional[SessionDetailResponse]:
        session, course_name = (
            db.query(
                Session,
                Course.title.label('course_name')
            )
            .join(Course, Session.course_id == Course.id)
            .filter(Session.id == session_id)
            .first()
        )

        if not session:
            return None

        course_status = calculate_course_status(session.begin_date, session.end_date)

        # Count lectures for this session
        lecture_count = (
            db.query(Lecture)
            .filter(Lecture.session_id == session.id)
            .count()
        )

        return SessionDetailResponse(**{
            "id": session.id,
            "title": session.title,
            "description": session.description,
            "lecturer_info": session.lecturer_info,
            "date_info": session.date_info,
            "begin_date": session.begin_date,
            "end_date": session.end_date,
            "course_id": session.course_id,
            "course_name": course_name,
            "course_status": course_status,
            "lecture_count": lecture_count,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "created_by": session.created_by,
            "updated_by": session.updated_by
        })

    @staticmethod
    def get_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[Session]:
        return db.query(Session).filter(Session.is_active == True).order_by(Session.created_at.desc()).offset(
            skip).limit(limit).all()

    @staticmethod
    def get_sessions_with_details(db: Session, skip: int = 0, limit: int = 100) -> List[SessionDetailResponse]:
        """Get sessions with course_name, course_status, and total_lectures count"""
        results = (
            db.query(
                Session,
                Course.title.label('course_name')
            )
            .join(Course, Session.course_id == Course.id)
            .filter(Session.is_active == True)
            .order_by(Session.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        response_list = []
        for session, course_name in results:
            course_status = calculate_course_status(session.begin_date, session.end_date)

            # Count lectures for this session
            lecture_count = (
                db.query(Lecture)
                .filter(Lecture.session_id == session.id)
                .count()
            )

            response_data = {
                "id": session.id,
                "title": session.title,
                "description": session.description,
                "lecturer_info": session.lecturer_info,
                "date_info": session.date_info,
                "begin_date": session.begin_date,
                "end_date": session.end_date,
                "course_id": session.course_id,
                "course_name": course_name,
                "course_status": course_status,
                "lecture_count": lecture_count,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
                "created_by": session.created_by,
                "updated_by": session.updated_by
            }
            response_list.append(SessionDetailResponse(**response_data))

        return response_list

    @staticmethod
    def get_sessions_by_course(db: Session, course_id: UUID, skip: int = 0, limit: int = 100) -> List[Session]:
        return db.query(Session).filter(Session.course_id == course_id, Session.is_active == True).order_by(
            Session.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_session(db: Session, session_data: SessionCreate, user: User) -> Session:
        session_dict = session_data.model_dump()
        session_dict['created_by'] = str(user.id)
        session_dict['updated_by'] = str(user.id)

        db_session = Session(**session_dict)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def update_session(db: Session, session_id: UUID, session_update: SessionUpdate) -> Optional[Session]:
        db_session = db.query(Session).filter(Session.id == session_id).first()
        if db_session:
            for field, value in session_update.model_dump(exclude_unset=True).items():
                setattr(db_session, field, value)
            db.commit()
            db.refresh(db_session)
        return db_session

    @staticmethod
    def delete_session(db: Session, session_id: UUID) -> bool:
        db_session = db.query(Session).filter(Session.id == session_id).first()
        if db_session:
            db_session.is_active = False
            db.commit()
            return True
        return False
