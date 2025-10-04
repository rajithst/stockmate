import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.engine import Base
from app.db.engine import get_db  # your normal get_db dependency
from tests.test_db import TestingSessionLocal, init_test_db, engine


# Override get_db for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

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

