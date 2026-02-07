from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from app.utils.security import create_access_token
from app.crud.user import UserCRUD
from app.crud.course import CourseCRUD
from app.crud.session import SessionCRUD
from app.schemas.user import UserCreate
from app.schemas.course import CourseCreate
from app.schemas.session import SessionCreate, SessionUpdate


class TestSessionAPI:
    """Test session API endpoints"""

    def test_create_session(self, client: TestClient, db_session):
        """Test creating a new session"""
        user_data = {
            "username": "session_creator",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Test Course",
            "description": "A test course",
            "keyword": "test",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "John Doe",
            "date_info": "2024-01-01 ~ 2024-02-01"
        }
        response = client.post(
            "/api/sessions",
            json=session_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Session"
        assert data["lecturer_info"] == "John Doe"

    def test_get_sessions(self, client: TestClient, db_session):
        """Test getting all sessions"""
        user_data = {
            "username": "session_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Sessions",
            "description": "Course description",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session 1",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        response = client.get("/api/sessions")

        assert response.status_code == 200
        sessions = response.json()
        assert len(sessions) >= 1

    def test_get_session_by_id(self, client: TestClient, db_session):
        """Test getting a specific session by ID"""
        user_data = {
            "username": "session_finder",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Session",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Specific Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-02"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        response = client.get(f"/api/sessions/{session.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Specific Session"

    def test_update_session(self, client: TestClient, db_session):
        """Test updating a session"""
        user_data = {
            "username": "session_updater",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Update",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Original Title",
            "lecturer_info": "Original Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        update_data = {
            "title": "Updated Title",
            "lecturer_info": "Updated Instructor",
            "updated_by": str(user.id)
        }
        response = client.put(
            f"/api/sessions/{session.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    def test_delete_session(self, client: TestClient, db_session):
        """Test deleting (deactivating) a session"""
        user_data = {
            "username": "session_deleter",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Delete",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Session to Delete",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        response = client.delete(
            f"/api/sessions/{session.id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Session deactivated successfully"}

    def test_get_session_not_found(self, client: TestClient):
        """Test getting non-existent session"""
        fake_id = uuid4()
        response = client.get(f"/api/sessions/{fake_id}")
        assert response.status_code == 404