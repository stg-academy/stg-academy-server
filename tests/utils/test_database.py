from app.database import Base, engine, get_db
from app.models.user import User


class TestDatabase:
    """Test database configuration"""

    def test_base_metadata(self):
        """Test that Base has metadata"""
        assert Base.metadata is not None

    def test_engine_exists(self):
        """Test that database engine exists"""
        assert engine is not None

    def test_get_db_generator(self):
        """Test that get_db is a generator function"""
        db_gen = get_db()
        assert db_gen is not None