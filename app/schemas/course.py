from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    keyword: Optional[str] = None
    is_active: bool = True

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keyword: Optional[str] = None
    is_active: Optional[bool] = None

class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str