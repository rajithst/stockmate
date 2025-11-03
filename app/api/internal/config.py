"""
Centralized configuration and constants for internal sync APIs.

Consolidates all hardcoded values, defaults, and enums used across
sync API endpoints to enable consistent behavior and easy customization.
"""

from typing import Final

# ========== API DEFAULTS ==========

# Default pagination/limit values (must be between min and max)
DEFAULTS: Final = {
    "financial_limit": 40,  # balance sheets, income statements, cash flows
    "metrics_limit": 40,  # key metrics, financial ratios
    "news_limit": 100,  # stock news, price target news, grading news
    "general_news_limit": 100,  # general market news
    "grading_limit": 50,  # gradings
    "price_target_limit": 50,  # price targets
    "stock_info_limit": 50,  # dividends, splits, peers
}

# ========== API CONSTRAINTS ==========

LIMITS: Final = {
    "financial_limit": {"min": 1, "max": 100},
    "metrics_limit": {"min": 1, "max": 100},
    "news_limit": {"min": 1, "max": 1000},
    "general_news_limit": {"min": 1, "max": 1000},
    "grading_limit": {"min": 1, "max": 500},
    "price_target_limit": {"min": 1, "max": 500},
    "stock_info_limit": {"min": 1, "max": 500},
}

# ========== PERIOD ENUMS ==========

PERIOD_TYPES: Final = {
    "financial": ["annual", "quarter"],
    "metrics": ["annual", "quarter"],
}

PERIOD_OPTIONS_ALL: Final = ["Q1", "Q2", "Q3", "Q4", "FY", "annual", "quarter"]

# ========== HTTP STATUS MESSAGES ==========

ERROR_MESSAGES: Final = {
    "NOT_FOUND_GENERIC": "Data not found for symbol: {symbol}",
    "NOT_FOUND_BALANCE_SHEETS": "Balance sheets not found for symbol: {symbol}",
    "NOT_FOUND_INCOME_STATEMENTS": "Income statements not found for symbol: {symbol}",
    "NOT_FOUND_CASH_FLOW": "Cash flow statements not found for symbol: {symbol}",
    "NOT_FOUND_FINANCIAL_HEALTH": "Financial health data not found for symbol: {symbol}",
    "NOT_FOUND_KEY_METRICS": "Key metrics not found for symbol: {symbol}",
    "NOT_FOUND_FINANCIAL_RATIOS": "Financial ratios not found for symbol: {symbol}",
    "NOT_FOUND_FINANCIAL_SCORES": "Financial scores not found for symbol: {symbol}",
    "NOT_FOUND_DCF": "Discounted cash flow not found for symbol: {symbol}",
    "NOT_FOUND_GRADINGS": "Gradings not found for symbol: {symbol}",
    "NOT_FOUND_RATING_SUMMARY": "Rating summary not found for symbol: {symbol}",
    "NOT_FOUND_PRICE_TARGETS": "Price targets not found for symbol: {symbol}",
    "NOT_FOUND_PRICE_TARGET_SUMMARY": "Price target summary not found for symbol: {symbol}",
    "NOT_FOUND_STOCK_NEWS": "Stock news not found for symbol: {symbol}",
    "NOT_FOUND_GENERAL_NEWS": "General news not found for given date range",
    "NOT_FOUND_PRICE_TARGET_NEWS": "Price target news not found for symbol: {symbol}",
    "NOT_FOUND_GRADING_NEWS": "Grading news not found for symbol: {symbol}",
    "NOT_FOUND_PRICE_CHANGES": "Price changes not found for symbol: {symbol}",
    "NOT_FOUND_DIVIDENDS": "Dividends not found for range: {from_date} to {to_date}",
    "NOT_FOUND_STOCK_SPLITS": "Stock splits not found for symbol: {symbol}",
    "NOT_FOUND_STOCK_PEERS": "Stock peers not found for symbol: {symbol}",
    "INVALID_SYMBOL": "Invalid stock symbol. Must be 1-5 characters",
    "NOT_FOUND_DAILY_PRICES": "Daily prices not found for symbol: {symbol}",
}

# ========== SUCCESS MESSAGES ==========

SUCCESS_MESSAGES: Final = {
    "SYNC_SUCCESS": "Successfully synced {count} {data_type} record(s) for {symbol}",
}

# ========== VALIDATIONS ==========

SYMBOL_CONSTRAINTS: Final = {
    "min_length": 1,
    "max_length": 5,
    "uppercase_only": True,
}

# ========== TAG DEFINITIONS (for OpenAPI docs) ==========

TAGS: Final = {
    "company": {"name": "company_data", "description": "Company profile data"},
    "financial": {
        "name": "financial_data",
        "description": "Financial statements and metrics",
    },
    "metrics": {
        "name": "metrics_data",
        "description": "Key metrics and financial ratios",
    },
    "news": {"name": "news_data", "description": "Market and company news"},
    "grading": {"name": "grading_data", "description": "Company gradings"},
    "rating": {"name": "rating_data", "description": "Company ratings"},
    "price_target": {
        "name": "price_target_data",
        "description": "Price targets and predictions",
    },
    "quotes": {
        "name": "quotes_data",
        "description": "Stock price quotes and changes",
    },
    "stock_info": {
        "name": "stock_info_data",
        "description": "Stock information (dividends, splits, peers)",
    },
    "dcf": {
        "name": "dcf_data",
        "description": "Discounted cash flow valuation",
    },
}
