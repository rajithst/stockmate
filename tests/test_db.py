from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.db.engine import Base


DATABASE_URL = "sqlite:///./test_stockmate.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Ensures same connection for all tests (important for SQLite)
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_test_db():
    """
    Create all tables for testing.
    Safe to call before tests.
    """
    Base.metadata.drop_all(bind=engine)  # ensure clean start
    Base.metadata.create_all(bind=engine)
