from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from ..models.user import Attendance, User
from ..schemas.attendance import AttendanceCreate, AttendanceUpdate

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