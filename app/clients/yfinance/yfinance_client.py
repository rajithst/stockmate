from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import pandas as pd

import yfinance as yf

from app.clients.yfinance.models.company import YFinanceCompanyProfile
from app.util.logs import setup_logger

logger = setup_logger(__name__)


# Custom Exception Classes
class YFinanceError(Exception):
    """Base exception for yfinance client errors"""

    pass


class YFinanceSymbolError(YFinanceError):
    """Raised when symbol is invalid or not found"""

    pass


class YFinanceDataError(YFinanceError):
    """Raised when data is unavailable or invalid"""

    pass


class YFinanceNetworkError(YFinanceError):
    """Raised for network-related errors"""

    pass


@dataclass
class YFinanceConfig:
    """Configuration for yfinance client"""

    timeout: int = 10
    max_retries: int = 3
    backoff_factor: float = 1.0
    progress: bool = False


class YFinanceClient:
    """Client for fetching stock data from yfinance API.

    Optimized for Japanese stocks (TSE - Tokyo Stock Exchange) but works for any stock.
    """

    def __init__(self, config: Optional[YFinanceConfig] = None):
        self.config = config or YFinanceConfig()
        self._cache: Dict[str, Any] = {}

    def _parse_datetime_to_datetime(self, date_val: Any) -> datetime:
        """Convert various date formats to datetime object."""
        if isinstance(date_val, datetime):
            return date_val
        elif isinstance(date_val, pd.Timestamp):
            return date_val.to_pydatetime()
        elif isinstance(date_val, str):
            try:
                return datetime.fromisoformat(date_val)
            except ValueError:
                try:
                    return pd.to_datetime(date_val).to_pydatetime()
                except Exception as e:
                    logger.error(f"Failed to parse date: {date_val}. Error: {e}")
                    raise YFinanceDataError(f"Invalid date format: {date_val}")
        else:
            return pd.to_datetime(date_val).to_pydatetime()

    def _get_ticker(self, symbol: str) -> yf.Ticker:
        """Get yfinance Ticker object with error handling."""
        try:
            ticker = yf.Ticker(symbol)
            # Try to get basic info - some may return empty info but still have history
            return ticker
        except Exception as e:
            logger.error(f"Failed to get ticker for {symbol}: {e}")
            raise YFinanceSymbolError(f"Invalid symbol or network error: {symbol}")

    def get_company_profile(self, symbol: str) -> Optional[YFinanceCompanyProfile]:
        """Fetches company information for a given stock symbol."""
        try:
            ticker = self._get_ticker(symbol)
            info = ticker.get_info()

            if not info:
                logger.warning(f"No company info available for {symbol}")
                return None

            try:
                company_info = YFinanceCompanyProfile.model_validate(info)
                return company_info
            except Exception as e:
                logger.error(f"Failed to parse company info for {symbol}: {e}")
                return None

        except YFinanceSymbolError:
            raise
        except Exception as e:
            logger.error(f"Error fetching company info for {symbol}: {e}")
            raise YFinanceDataError(f"Failed to fetch company info: {e}")
