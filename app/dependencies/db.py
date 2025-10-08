from app.db.engine import SessionLocal
from sqlalchemy.orm import Session

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
