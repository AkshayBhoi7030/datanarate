import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.repositories.base import BaseRepository
from uuid import UUID, uuid4
from app.models.saved_query import SavedQuery


@pytest.fixture(scope="function")
def db_session():
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_base_repository_create(db_session):
    repo = BaseRepository(SavedQuery, db_session)
    data = {
        "id": uuid4(),
        "user_id": uuid4(),
        "name": "Test Query",
        "natural_language_query": "Show me all data",
        "generated_sql": "SELECT * FROM table"
    }
    obj = repo.create(data)
    assert obj.id == data["id"]
    assert obj.name == "Test Query"


def test_base_repository_get(db_session):
    repo = BaseRepository(SavedQuery, db_session)
    test_id = uuid4()
    data = {
        "id": test_id,
        "user_id": uuid4(),
        "name": "Test Query",
        "natural_language_query": "Show me all data",
        "generated_sql": "SELECT * FROM table"
    }
    repo.create(data)
    obj = repo.get(test_id)
    assert obj is not None
    assert obj.id == test_id


def test_base_repository_update(db_session):
    repo = BaseRepository(SavedQuery, db_session)
    test_id = uuid4()
    data = {
        "id": test_id,
        "user_id": uuid4(),
        "name": "Test Query",
        "natural_language_query": "Show me all data",
        "generated_sql": "SELECT * FROM table"
    }
    obj = repo.create(data)
    updated_obj = repo.update(obj, {"name": "Updated Query"})
    assert updated_obj.name == "Updated Query"


def test_base_repository_remove(db_session):
    repo = BaseRepository(SavedQuery, db_session)
    test_id = uuid4()
    data = {
        "id": test_id,
        "user_id": uuid4(),
        "name": "Test Query",
        "natural_language_query": "Show me all data",
        "generated_sql": "SELECT * FROM table"
    }
    repo.create(data)
    removed = repo.remove(test_id)
    assert removed is not None
    assert repo.get(test_id) is None


def test_base_repository_get_multi(db_session):
    repo = BaseRepository(SavedQuery, db_session)
    for i in range(5):
        data = {
            "id": uuid4(),
            "user_id": uuid4(),
            "name": f"Test Query {i}",
            "natural_language_query": "Show me all data",
            "generated_sql": "SELECT * FROM table"
        }
        repo.create(data)
    items = repo.get_multi(skip=0, limit=3)
    assert len(items) == 3


def test_base_repository_get_nonexistent(db_session):
    repo = BaseRepository(SavedQuery, db_session)
    obj = repo.get(uuid4())
    assert obj is None


def test_base_repository_remove_nonexistent(db_session):
    repo = BaseRepository(SavedQuery, db_session)
    removed = repo.remove(uuid4())
    assert removed is None
