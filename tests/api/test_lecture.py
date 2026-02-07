from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from app.utils.security import create_access_token
from app.crud.user import UserCRUD
from app.crud.course import CourseCRUD
from app.crud.session import SessionCRUD
from app.crud.lecture import LectureCRUD
from app.schemas.user import UserCreate
from app.schemas.course import CourseCreate
from app.schemas.session import SessionCreate
from app.schemas.lecture import LectureCreate, LectureUpdate


class TestLectureAPI:
    """Test lecture API endpoints"""

    def test_create_lecture(self, client: TestClient, db_session):
        """Test creating a new lecture"""
        user_data = {
            "username": "lecture_creator",
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

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        lecture_data = {
            "session_id": str(session.id),
            "title": "Test Lecture",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        response = client.post(
            "/api/lectures",
            json=lecture_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Lecture"
        assert data["sequence"] == 1

    def test_get_lectures(self, client: TestClient, db_session):
        """Test getting all lectures"""
        user_data = {
            "username": "lecture_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Lectures",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        lecture_data = {
            "session_id": str(session.id),
            "title": "Test Lecture 1",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        response = client.get("/api/lectures")

        assert response.status_code == 200
        lectures = response.json()
        assert len(lectures) >= 1

    def test_get_lectures_by_session(self, client: TestClient, db_session):
        """Test getting lectures by session ID"""
        user_data = {
            "username": "session_lectures_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Session Lectures",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        lecture_data_1 = {
            "session_id": str(session.id),
            "title": "First Lecture",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data_1), user)

        lecture_data_2 = {
            "session_id": str(session.id),
            "title": "Second Lecture",
            "sequence": 2,
            "attendance_type": "offline",
            "lecture_date": datetime.utcnow().isoformat()
        }
        LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data_2), user)

        response = client.get(f"/api/lectures/session/{session.id}")

        assert response.status_code == 200
        lectures = response.json()
        assert len(lectures) == 2

    def test_get_lecture_by_id(self, client: TestClient, db_session):
        """Test getting a specific lecture by ID"""
        user_data = {
            "username": "lecture_finder",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Lecture",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        lecture_data = {
            "session_id": str(session.id),
            "title": "Specific Lecture",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        lecture = LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        response = client.get(f"/api/lectures/{lecture.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Specific Lecture"

    def test_update_lecture(self, client: TestClient, db_session):
        """Test updating a lecture"""
        user_data = {
            "username": "lecture_updater",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Update Lecture",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        lecture_data = {
            "session_id": str(session.id),
            "title": "Original Title",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        lecture = LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        update_data = {
            "title": "Updated Title",
            "attendance_type": "offline",
            "updated_by": str(user.id)
        }
        response = client.put(
            f"/api/lectures/{lecture.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["attendance_type"] == "offline"

    def test_delete_lecture(self, client: TestClient, db_session):
        """Test deleting (deactivating) a lecture"""
        user_data = {
            "username": "lecture_deleter",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Delete Lecture",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        lecture_data = {
            "session_id": str(session.id),
            "title": "Lecture to Delete",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        lecture = LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        response = client.delete(
            f"/api/lectures/{lecture.id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Lecture deactivated successfully"}

    def test_get_lecture_not_found(self, client: TestClient):
        """Test getting non-existent lecture"""
        fake_id = uuid4()
        response = client.get(f"/api/lectures/{fake_id}")
        assert response.status_code == 404