from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import config

# ---------------------------------------------------------
# 1️⃣  Build database engine
# ---------------------------------------------------------
# For MySQL (production)
connect_args = {}

# SQLite requires special args
if config.db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    config.db_url,
    pool_pre_ping=True,  # ✅ avoids stale connections in MySQL
    connect_args=connect_args,
)

# ---------------------------------------------------------
# 2️⃣  Session factory
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ---------------------------------------------------------
# 3️⃣  Declarative Base class
# ---------------------------------------------------------
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy schemas."""
    pass


# ---------------------------------------------------------
# 4️⃣  Dependency for FastAPI routes
# ---------------------------------------------------------
def get_db():
    """Provide a new database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
