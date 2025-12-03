"""yfinance client module for fetching stock data from Yahoo Finance.

Optimized for Japanese stocks but works for any stock globally.
"""

from app.clients.yfinance.yfinance_client import (
    YFinanceClient,
    YFinanceConfig,
    YFinanceError,
    YFinanceSymbolError,
    YFinanceDataError,
    YFinanceNetworkError,
)
from app.clients.yfinance.protocol import YFinanceClientProtocol

__all__ = [
    "YFinanceClient",
    "YFinanceConfig",
    "YFinanceClientProtocol",
    "YFinanceError",
    "YFinanceSymbolError",
    "YFinanceDataError",
    "YFinanceNetworkError",
]
