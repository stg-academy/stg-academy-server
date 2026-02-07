from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from ..models.user import Session, User
from ..schemas.session import SessionCreate, SessionUpdate

class SessionCRUD:
    @staticmethod
    def get_session(db: Session, session_id: UUID) -> Optional[Session]:
        return db.query(Session).filter(Session.id == session_id).first()

    @staticmethod
    def get_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[Session]:
        return db.query(Session).filter(Session.is_active == True).order_by(Session.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_sessions_by_course(db: Session, course_id: UUID, skip: int = 0, limit: int = 100) -> List[Session]:
        return db.query(Session).filter(Session.course_id == course_id, Session.is_active == True).order_by(Session.created_at.desc()).offset(skip).limit(limit).all()

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