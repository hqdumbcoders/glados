import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

# 1. Connect to the test database
TEST_DATABASE_URL = "postgresql+psycopg2://glados_user:glados_password@localhost:5433/glados_test_db"

engine = create_engine(TEST_DATABASE_URL)

# 2. Create the test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Fixture to create tables before tests and drop them after
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine) # Create tables
    yield
    Base.metadata.drop_all(bind=engine) # Drop tables after all tests

# 4. Fixture that overrides the real database with the test one
@pytest.fixture()
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

# 5. Fixture for the test client
@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()