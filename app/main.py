from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.internal import (
    company_full_data_sync,
    company_metrics_sync,
    company_sync,
    financial_health_sync,
    financials_statements_sync,
    market_data_sync,
    pubsub_handler_api,
    quotes_sync,
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
    company_sync.router, prefix="/api/internal/company-sync", tags=["company-sync"]
)
app.include_router(
    company_full_data_sync.router,
    prefix="/api/internal/company-full-data-sync",
    tags=["company-full-data-sync"],
)
app.include_router(
    company_metrics_sync.router,
    prefix="/api/internal/company-metrics-sync",
    tags=["company-metrics-sync"],
)
app.include_router(
    financial_health_sync.router,
    prefix="/api/internal/financial-health-sync",
    tags=["financial-health-sync"],
)
app.include_router(
    financials_statements_sync.router,
    prefix="/api/internal/financials-statements-sync",
    tags=["financials-statements-sync"],
)
app.include_router(
    market_data_sync.router,
    prefix="/api/internal/market-data-sync",
    tags=["market-data-sync"],
)

app.include_router(
    quotes_sync.router,
    prefix="/api/internal/quotes-sync",
    tags=["quotes-sync"],
)

# Include Pub/Sub webhook endpoint
app.include_router(
    pubsub_handler_api.router,
    prefix="/api/internal/pubsub",
    tags=["pubsub"],
)
