from fastapi import FastAPI

from app.api.v1 import company
from app.core.config import config
from app.core.logs import setup_logging
from app.db.engine import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name, debug=config.debug)

app.include_router(company.router, prefix="/api/v1", tags=["company"])