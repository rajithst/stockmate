import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.db.engine import Base
from app.main import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DATABASE_URL = "sqlite:///./test_stockmate.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provide a fresh DB session for each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "api: mark test as an API test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "database: mark test as requiring database")
    config.addinivalue_line(
        "markers", "external: mark test as requiring external services"
    )


@pytest.fixture
def performance_monitor():
    """Fixture for monitoring test performance."""
    import time

    start_time = time.time()

    yield

    end_time = time.time()
    execution_time = end_time - start_time

    # Log slow tests (> 3 seconds)
    if execution_time > 3.0:
        print(f"\nSlow test detected: {execution_time:.2f}s")


@pytest.fixture
def assert_no_logs(caplog):
    """Fixture to assert that no logs were generated."""
    yield
    assert len(caplog.records) == 0, (
        f"Unexpected log messages: {[r.message for r in caplog.records]}"
    )


@pytest.fixture
def assert_no_warnings():
    """Fixture to assert that no warnings were generated."""
    import warnings

    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")
        yield warning_list

    assert len(warning_list) == 0, (
        f"Unexpected warnings: {[str(w.message) for w in warning_list]}"
    )


@pytest.fixture
def memory_monitor():
    """Monitor memory usage during test execution."""
    import os

    import psutil

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    yield

    final_memory = process.memory_info().rss
    memory_diff = final_memory - initial_memory

    # Log significant memory increases (> 10MB)
    if memory_diff > 10 * 1024 * 1024:
        print(f"\nHigh memory usage detected: +{memory_diff / 1024 / 1024:.1f}MB")
