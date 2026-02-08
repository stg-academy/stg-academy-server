from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class SessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    lecturer_info: Optional[str] = None
    date_info: Optional[str] = None
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class SessionCreate(SessionBase):
    course_id: UUID

class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    lecturer_info: Optional[str] = None
    date_info: Optional[str] = None
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class SessionResponse(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID

class SessionDetailResponse(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    course_name: str
    course_status: str
    lecture_count: int
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID