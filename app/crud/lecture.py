from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from ..models.user import Lecture, User
from ..schemas.lecture import LectureCreate, LectureUpdate

class LectureCRUD:
    @staticmethod
    def get_lecture(db: Session, lecture_id: UUID) -> Optional[Lecture]:
        return db.query(Lecture).filter(Lecture.id == lecture_id).first()

    @staticmethod
    def get_lectures(db: Session, skip: int = 0, limit: int = 100) -> List[Lecture]:
        return db.query(Lecture).offset(skip).limit(limit).all()

    @staticmethod
    def get_lectures_by_session(db: Session, session_id: UUID, skip: int = 0, limit: int = 100) -> List[Lecture]:
        return db.query(Lecture).filter(Lecture.session_id == session_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_lecture(db: Session, lecture: LectureCreate, user: User) -> Lecture:
        lecture_dict = lecture.model_dump()
        lecture_dict['created_by'] = str(user.id)
        lecture_dict['updated_by'] = str(user.id)

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

    @staticmethod
    def delete_lecture(db: Session, lecture_id: UUID) -> bool:
        db_lecture = db.query(Lecture).filter(Lecture.id == lecture_id).first()
        if db_lecture:
            db.delete(db_lecture)
            db.commit()
            return True
        return False