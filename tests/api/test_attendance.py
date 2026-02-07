from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from app.utils.security import create_access_token
from app.crud.user import UserCRUD
from app.crud.course import CourseCRUD
from app.crud.session import SessionCRUD
from app.crud.lecture import LectureCRUD
from app.crud.attendance import AttendanceCRUD
from app.schemas.user import UserCreate
from app.schemas.course import CourseCreate
from app.schemas.session import SessionCreate
from app.schemas.lecture import LectureCreate
from app.schemas.attendance import AttendanceCreate


class TestAttendanceAPI:
    """Test attendance API endpoints"""

    def test_create_attendance(self, client: TestClient, db_session):
        """Test creating attendance for a lecture"""
        user_data = {
            "username": "attendance_creator",
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

        lecture_data = {
            "session_id": str(session.id),
            "title": "Test Lecture",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        lecture = LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        attendance_data = {
            "user_id": str(user.id),
            "status": "present",
            "detail_type": "online",
            "description": "Attended online"
        }
        response = client.post(
            f"/api/attendances/lectures/{lecture.id}/attendances",
            json=attendance_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "present"
        assert data["detail_type"] == "online"

    def test_get_attendances_by_lecture(self, client: TestClient, db_session):
        """Test getting all attendances for a lecture"""
        user_data = {
            "username": "attendance_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Attendance",
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
            "title": "Test Lecture",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        lecture = LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        attendance_data = {
            "user_id": str(user.id),
            "status": "present",
            "detail_type": "online",
            "description": "Attended"
        }
        AttendanceCRUD.create_attendance(db_session, lecture.id, AttendanceCreate(**attendance_data), user)

        response = client.get(f"/api/attendances/lectures/{lecture.id}/attendances")

        assert response.status_code == 200
        attendances = response.json()
        assert len(attendances) >= 1

    def test_get_attendance_by_id(self, client: TestClient, db_session):
        """Test getting a specific attendance by ID"""
        user_data = {
            "username": "attendance_finder",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Attendance",
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
            "title": "Test Lecture",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        lecture = LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        attendance_data = {
            "user_id": str(user.id),
            "status": "present",
            "detail_type": "online",
            "description": "Specific attendance"
        }
        attendance = AttendanceCRUD.create_attendance(db_session, lecture.id, AttendanceCreate(**attendance_data), user)

        response = client.get(f"/api/attendances/{attendance.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Specific attendance"

    def test_update_attendance(self, client: TestClient, db_session):
        """Test updating an attendance record"""
        user_data = {
            "username": "attendance_updater",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Update Attendance",
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
            "title": "Test Lecture",
            "sequence": 1,
            "attendance_type": "online",
            "lecture_date": datetime.utcnow().isoformat()
        }
        lecture = LectureCRUD.create_lecture(db_session, LectureCreate(**lecture_data), user)

        attendance_data = {
            "user_id": str(user.id),
            "status": "absent",
            "detail_type": "offline",
            "description": "Original status"
        }
        attendance = AttendanceCRUD.create_attendance(db_session, lecture.id, AttendanceCreate(**attendance_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        update_data = {
            "status": "present",
            "description": "Updated status",
            "updated_by": str(user.id)
        }
        response = client.put(
            f"/api/attendances/{attendance.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "present"
        assert data["description"] == "Updated status"

    def test_get_attendance_not_found(self, client: TestClient):
        """Test getting non-existent attendance"""
        fake_id = uuid4()
        response = client.get(f"/api/attendances/{fake_id}")
        assert response.status_code == 404