from app.db.session import engine
from app.db.base import Base


def test_database_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            assert result.scalar() == 1
    except Exception as e:
        assert False, f"Database connection failed: {e}"
