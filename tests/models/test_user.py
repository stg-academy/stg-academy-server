import pytest
from datetime import datetime
from uuid import uuid4

from app.models.user import User, Course, Session, Lecture, Attendance, Certification


class TestUserModel:
    def test_create_user(self, db_session):
        user = User(
            username="testuser",
            auth_type="kakao",
            kakao_id="12345",
            authorizations={"role": "user"},
            is_active=True
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.auth_type == "kakao"
        assert user.kakao_id == "12345"
        assert user.authorizations == {"role": "user"}
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_relationships(self, db_session):
        user = User(username="testuser", auth_type="test", is_active=True)
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)

        db_session.add_all([user, course])
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(course)

        # Test certification relationship
        certification = Certification(
            course_id=course.id,
            user_id=user.id,
            issued_at=datetime.utcnow(),
            created_by="admin",
            updated_by="admin"
        )
        db_session.add(certification)
        db_session.commit()

        # Test relationships
        assert len(user.certifications) == 1
        assert user.certifications[0].course_id == course.id


class TestCourseModel:
    def test_create_course(self, db_session):
        course = Course(
            title="Python Programming",
            description="Learn Python from basics",
            keyword="python,programming",
            created_by="admin",
            updated_by="admin",
            is_active=True
        )

        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        assert course.id is not None
        assert course.title == "Python Programming"
        assert course.description == "Learn Python from basics"
        assert course.keyword == "python,programming"
        assert course.is_active is True
        assert course.created_at is not None
        assert course.updated_at is not None

    def test_course_session_relationship(self, db_session):
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        session_obj = Session(
            course_id=course.id,
            title="Test Session",
            created_by="admin",
            updated_by="admin",
            is_active=True
        )
        db_session.add(session_obj)
        db_session.commit()

        assert len(course.sessions) == 1
        assert course.sessions[0].title == "Test Session"


class TestSessionModel:
    def test_create_session(self, db_session):
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        session_obj = Session(
            course_id=course.id,
            title="Advanced Python",
            lecturer_info="Dr. Smith",
            date_info="Monday-Wednesday",
            created_by="admin",
            updated_by="admin",
            is_active=True
        )

        db_session.add(session_obj)
        db_session.commit()
        db_session.refresh(session_obj)

        assert session_obj.id is not None
        assert session_obj.course_id == course.id
        assert session_obj.title == "Advanced Python"
        assert session_obj.lecturer_info == "Dr. Smith"
        assert session_obj.date_info == "Monday-Wednesday"
        assert session_obj.is_active is True

    def test_session_lecture_relationship(self, db_session):
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        session_obj = Session(course_id=course.id, title="Test Session", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(session_obj)
        db_session.commit()
        db_session.refresh(session_obj)

        lecture = Lecture(
            session_id=session_obj.id,
            title="Introduction",
            sequence=1,
            created_by="admin",
            updated_by="admin"
        )
        db_session.add(lecture)
        db_session.commit()

        assert len(session_obj.lectures) == 1
        assert session_obj.lectures[0].title == "Introduction"


class TestLectureModel:
    def test_create_lecture(self, db_session):
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        session_obj = Session(course_id=course.id, title="Test Session", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(session_obj)
        db_session.commit()
        db_session.refresh(session_obj)

        lecture = Lecture(
            session_id=session_obj.id,
            title="Variables and Data Types",
            sequence=1,
            attendance_type="mandatory",
            created_by="admin",
            updated_by="admin"
        )

        db_session.add(lecture)
        db_session.commit()
        db_session.refresh(lecture)

        assert lecture.id is not None
        assert lecture.session_id == session_obj.id
        assert lecture.title == "Variables and Data Types"
        assert lecture.sequence == 1
        assert lecture.attendance_type == "mandatory"

    def test_lecture_attendance_relationship(self, db_session):
        user = User(username="student", auth_type="test", is_active=True)
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)

        db_session.add_all([user, course])
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(course)

        session_obj = Session(course_id=course.id, title="Test Session", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(session_obj)
        db_session.commit()
        db_session.refresh(session_obj)

        lecture = Lecture(session_id=session_obj.id, title="Test Lecture", sequence=1, created_by="admin", updated_by="admin")
        db_session.add(lecture)
        db_session.commit()
        db_session.refresh(lecture)

        attendance = Attendance(
            lecture_id=lecture.id,
            user_id=user.id,
            status="present",
            created_by="admin",
            updated_by="admin"
        )
        db_session.add(attendance)
        db_session.commit()

        assert len(lecture.attendances) == 1
        assert lecture.attendances[0].status == "present"


class TestAttendanceModel:
    def test_create_attendance(self, db_session):
        user = User(username="student", auth_type="test", is_active=True)
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)

        db_session.add_all([user, course])
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(course)

        session_obj = Session(course_id=course.id, title="Test Session", created_by="admin", updated_by="admin", is_active=True)
        db_session.add(session_obj)
        db_session.commit()
        db_session.refresh(session_obj)

        lecture = Lecture(session_id=session_obj.id, title="Test Lecture", sequence=1, created_by="admin", updated_by="admin")
        db_session.add(lecture)
        db_session.commit()
        db_session.refresh(lecture)

        attendance = Attendance(
            lecture_id=lecture.id,
            user_id=user.id,
            status="late",
            detail_type="traffic",
            description="Traffic jam on highway",
            created_by="admin",
            updated_by="admin"
        )

        db_session.add(attendance)
        db_session.commit()
        db_session.refresh(attendance)

        assert attendance.id is not None
        assert attendance.lecture_id == lecture.id
        assert attendance.user_id == user.id
        assert attendance.status == "late"
        assert attendance.detail_type == "traffic"
        assert attendance.description == "Traffic jam on highway"


class TestCertificationModel:
    def test_create_certification(self, db_session):
        user = User(username="student", auth_type="test", is_active=True)
        course = Course(title="Test Course", created_by="admin", updated_by="admin", is_active=True)

        db_session.add_all([user, course])
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(course)

        certification = Certification(
            course_id=course.id,
            user_id=user.id,
            session_ids=["session1", "session2"],
            issued_at=datetime.utcnow(),
            created_by="admin",
            updated_by="admin"
        )

        db_session.add(certification)
        db_session.commit()
        db_session.refresh(certification)

        assert certification.id is not None
        assert certification.course_id == course.id
        assert certification.user_id == user.id
        assert certification.session_ids == ["session1", "session2"]
        assert certification.issued_at is not None