from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class AttendanceBase(BaseModel):
    status: str
    detail_type: Optional[str] = None
    description: Optional[str] = None
    assignment_id: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    user_id: UUID

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    detail_type: Optional[str] = None
    description: Optional[str] = None
    assignment_id: Optional[str] = None
    updated_by: UUID

class AttendanceResponse(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lecture_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID