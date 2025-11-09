from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.internal import (
    analyst_estimate_sync,
    company_full_data_sync,
    company_sync,
    dcf_sync,
    financials_sync,
    grading_sync,
    metrics_sync,
    news_sync,
    price_target_sync,
    quotes_sync,
    rating_sync,
    revenue_product_segmentation_sync,
    stock_info_sync,
)
from app.api.v1 import auth, company, portfolio, watchlist
from app.core.config import config
from app.core.logs import setup_logging

setup_logging()

app = FastAPI(title=config.app_name, debug=config.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Or specify specific methods like ["GET", "POST"]
    allow_headers=["*"],  # Or specify specific headers
)

app.include_router(company.router, prefix="/api/v1/company", tags=["company"])
app.include_router(watchlist.router, prefix="/api/v1/watchlist", tags=["watchlist"])

app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["portfolio"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(
    company_sync.router, prefix="/api/internal/company", tags=["company_data"]
)
app.include_router(
    company_full_data_sync.router,
    prefix="/api/internal/company",
    tags=["company_data"],
)
app.include_router(
    financials_sync.router, prefix="/api/internal/financials", tags=["financial_data"]
)
app.include_router(news_sync.router, prefix="/api/internal/news", tags=["news_data"])
app.include_router(
    grading_sync.router, prefix="/api/internal/grading", tags=["grading_data"]
)
app.include_router(
    metrics_sync.router, prefix="/api/internal/metrics", tags=["metrics_data"]
)
app.include_router(
    price_target_sync.router,
    prefix="/api/internal/price_target",
    tags=["price_target_data"],
)
app.include_router(
    rating_sync.router, prefix="/api/internal/rating", tags=["rating_data"]
)
app.include_router(
    stock_info_sync.router, prefix="/api/internal/stock_info", tags=["stock_info_data"]
)
app.include_router(dcf_sync.router, prefix="/api/internal/dcf", tags=["dcf_data"])
app.include_router(
    quotes_sync.router, prefix="/api/internal/quotes", tags=["quotes_data"]
)
app.include_router(
    analyst_estimate_sync.router,
    prefix="/api/internal/analyst-estimates",
    tags=["analyst_estimates_data"],
)
app.include_router(
    revenue_product_segmentation_sync.router,
    prefix="/api/internal/revenue-segmentation",
    tags=["revenue_segmentation_data"],
)
