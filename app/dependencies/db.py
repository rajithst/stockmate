from app.db.engine import SessionLocal


def get_db_session():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
