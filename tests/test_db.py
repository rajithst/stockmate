import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.engine import Base
from app.db.engine import get_db


DATABASE_URL = "sqlite:///./test_stockmate.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Ensures same connection for all tests (important for SQLite)
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_test_db():
    """
    Create all tables for testing.
    Safe to call before tests.
    """
    Base.metadata.drop_all(bind=engine)  # ensure clean start
    Base.metadata.create_all(bind=engine)

# Apply the override
app.dependency_overrides[get_db] = override_get_db # type: ignore[attr-defined]


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test DB schema once before all tests."""
    init_test_db()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Return a test client that uses the overridden test DB."""
    return TestClient(app)
