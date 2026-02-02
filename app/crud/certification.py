from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from ..models.user import Certification, User
from ..schemas.certification import CertificationCreate, CertificationUpdate

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