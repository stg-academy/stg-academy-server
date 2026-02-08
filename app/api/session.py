from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..models.user import User
from ..schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionDetailResponse
from ..crud.session import SessionCRUD
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

@router.post("", response_model=SessionResponse)
async def create_session(
        session_data: SessionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return SessionCRUD.create_session(db, session_data, current_user)

@router.get("", response_model=List[SessionDetailResponse])
async def get_sessions(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    return SessionCRUD.get_sessions_with_details(db, skip=skip, limit=limit)

@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(
        session_id: UUID,
        db: Session = Depends(get_db)
):
    session_obj = SessionCRUD.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_obj

@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
        session_id: UUID,
        session_update: SessionUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    session_obj = SessionCRUD.update_session(db, session_id, session_update)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_obj

@router.delete("/{session_id}")
async def delete_session(
        session_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    success = SessionCRUD.delete_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deactivated successfully"}