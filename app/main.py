from fastapi import FastAPI

from app.api.internal import (
    company_sync,
    financials_sync,
    grading_sync,
    metrics_sync,
    news_sync,
    price_target_sync,
    rating_sync,
    stock_info_sync,
)
from app.api.v1 import company
from app.core.config import config
from app.core.logs import setup_logging

setup_logging()

app = FastAPI(title=config.app_name, debug=config.debug)

app.include_router(company.router, prefix="/api/v1", tags=["company"])
app.include_router(company_sync.router, prefix="/api/internal", tags=["company_data"])
app.include_router(
    financials_sync.router, prefix="/api/internal", tags=["financial_data"]
)
app.include_router(news_sync.router, prefix="/api/internal", tags=["news_data"])
app.include_router(grading_sync.router, prefix="/api/internal", tags=["grading_data"])
app.include_router(metrics_sync.router, prefix="/api/internal", tags=["metrics_data"])
app.include_router(
    price_target_sync.router, prefix="/api/internal", tags=["price_target_data"]
)
app.include_router(rating_sync.router, prefix="/api/internal", tags=["rating_data"])
app.include_router(
    stock_info_sync.router, prefix="/api/internal", tags=["stock_info_data"]
)
