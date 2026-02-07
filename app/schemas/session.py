from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class SessionBase(BaseModel):
    title: str
    lecturer_info: Optional[str] = None
    date_info: Optional[str] = None
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True

class SessionCreate(SessionBase):
    course_id: UUID

class SessionUpdate(BaseModel):
    title: Optional[str] = None
    lecturer_info: Optional[str] = None
    date_info: Optional[str] = None
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    updated_by: UUID

class SessionResponse(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID