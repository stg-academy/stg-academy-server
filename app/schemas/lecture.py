from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class LectureBase(BaseModel):
    title: str
    sequence: int
    attendance_type: Optional[str] = None
    lecture_date: Optional[datetime] = None

class LectureCreate(LectureBase):
    session_id: UUID

class LectureUpdate(BaseModel):
    title: Optional[str] = None
    sequence: Optional[int] = None
    attendance_type: Optional[str] = None
    lecture_date: Optional[datetime] = None

class LectureResponse(LectureBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID