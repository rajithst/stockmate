from typing import Any, Dict, Optional
import time
from dataclasses import dataclass

import requests

from app.clients.fmp.models.analyst_estimates import FMPAnalystEstimates
from app.clients.fmp.models.company import FMPCompanyProfile
from app.clients.fmp.models.discounted_cashflow import FMPDFCValuation
from app.clients.fmp.models.dividend import FMPDividend, FMPDividendCalendar
from app.clients.fmp.models.financial_ratios import (
    FMPFinancialRatios,
    FMPFinancialScores,
    FMPKeyMetrics,
)
from app.clients.fmp.models.financial_statements import (
    FMPCompanyBalanceSheet,
    FMPCompanyCashFlowStatement,
    FMPCompanyIncomeStatement,
)
from app.clients.fmp.models.news import (
    FMPGeneralNews,
    FMPPriceTargetNews,
    FMPStockGradingNews,
    FMPStockNews,
)
from app.clients.fmp.models.quotes import (
    FMPStockPrice,
    FMPStockPriceChange,
    FMPAfterHoursPrice,
    FMPStockHistoricalPrice,
)
from app.clients.fmp.models.revenue_product_segmentation import (
    FMPRevenueProductSegmentation,
)
from app.clients.fmp.models.stock import (
    FMPStockGrading,
    FMPStockGradingSummary,
    FMPStockPeer,
    FMPStockPriceTarget,
    FMPStockPriceTargetSummary,
    FMPStockRating,
    FMPStockScreenResult,
    FMPStockSplit,
)
from app.core.config import config
from app.util.logs import setup_logger

BASE_URL = "https://financialmodelingprep.com/stable"
IS_DEV = config.debug
logger = setup_logger(__name__)
PERIODS = {"quarter", "annual", "Q1", "Q2", "Q3", "Q4", "FY"}


# Custom Exception Classes
class FMPError(Exception):
    """Base exception for FMP client errors"""

    pass


class FMPRateLimitError(FMPError):
    """Raised when API rate limit is exceeded"""

    pass


class FMPTimeoutError(FMPError):
    """Raised when request times out"""

    pass


class FMPHTTPError(FMPError):
    """Raised for HTTP errors"""

    pass


class FMPConnectionError(FMPError):
    """Raised for connection errors"""

    pass


@dataclass
class FMPConfig:
    """Configuration for FMP client"""

    api_key: str
    base_url: str = "https://financialmodelingprep.com/stable"
    timeout: int = 10
    max_retries: int = 3
    backoff_factor: float = 1.0
    rate_limit_delay: float = 0.1


class FMPClient:
    def __init__(self, token, config: Optional[FMPConfig] = None):
        self.token = token
        self.config = config or FMPConfig(api_key=token)
        self.BASE_URL = self.config.base_url
        self.timeout = self.config.timeout
        self._last_request_time = 0

    def get_stock_screeners(self, params: dict) -> list[FMPStockScreenResult]:
        """Fetches stock screener results based on provided parameters.
        Args:
            params (Dict[str, any]): A dictionary of screener parameters.
        Returns:
            list: A list of stock screener results.
        """
        screener_params = {
            "market_cap_more_than": params.get("market_cap_more_than"),
            "market_cap_lower_than": params.get("market_cap_lower_than"),
            "beta_more_than": params.get("beta_more_than"),
            "beta_lower_than": params.get("beta_lower_than"),
            "volume_more_than": params.get("volume_more_than"),
            "volume_lower_than": params.get("volume_lower_than"),
            "price_more_than": params.get("price_more_than"),
            "price_lower_than": params.get("price_lower_than"),
            "dividend_more_than": params.get("dividend_more_than"),
            "dividend_lower_than": params.get("dividend_lower_than"),
            "is_actively_trading": params.get("is_actively_trading"),
            "exchange": params.get("exchange"),
            "sector": params.get("sector"),
            "industry": params.get("industry"),
            "country": params.get("country"),
            "limit": params.get("limit", 10),
        }
        stocks = self.__get_by_url(
            endpoint="company-screener",
            params={**screener_params},
        )
        return self._handle_list_response(stocks, FMPStockScreenResult)

    def get_company_profile(self, symbol: str) -> Optional[FMPCompanyProfile]:
        """Fetches the company profile for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the profile for.
        Returns:
            Optional[FMPCompanyProfile]: The company profile if found, else None.
        """
        profile = self.__get_by_url(endpoint="profile", params={"symbol": symbol})
        return self._handle_single_response(profile, FMPCompanyProfile)

    def get_income_statements(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> list[FMPCompanyIncomeStatement]:
        """Fetches the income statement for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the income statement for.
            period (str): The period for the income statement ('quarter' or 'annual').
            limit (int): The maximum number of records to fetch.
        Returns:
            list: A list of income statement records.
        """
        income_statements = self.__get_by_url(
            endpoint="income-statement",
            params={"symbol": symbol, "period": period, "limit": limit},
        )
        return self._handle_list_response(income_statements, FMPCompanyIncomeStatement)

    def get_balance_sheets(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> list[FMPCompanyBalanceSheet]:
        """Fetches the balance sheet for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the balance sheet for.
            period (str): The period for the balance sheet ('quarter' or 'annual').
            limit (int): The maximum number of records to fetch.
        Returns:
            list: A list of balance sheet records.
        """
        balance_sheets = self.__get_by_url(
            endpoint="balance-sheet-statement",
            params={"symbol": symbol, "period": period, "limit": limit},
        )
        return self._handle_list_response(balance_sheets, FMPCompanyBalanceSheet)

    def get_cash_flow_statements(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> list[FMPCompanyCashFlowStatement]:
        """Fetches the cash flow statement for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the cash flow statement for.
            period (str): The period for the cash flow statement ('quarter' or 'annual').
            limit (int): The maximum number of records to fetch.
        Returns:
            list: A list of cash flow statement records.
        """
        cash_flow_statements = self.__get_by_url(
            endpoint="cash-flow-statement",
            params={"symbol": symbol, "period": period, "limit": limit},
        )
        return self._handle_list_response(
            cash_flow_statements, FMPCompanyCashFlowStatement
        )

    def get_key_metrics(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> list[FMPKeyMetrics]:
        """Fetches key metrics for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the key metrics for.
            period (str): The period for the key metrics ('Q1','Q2','Q3','Q4','FY','annual','quarter').
            limit (int): The maximum number of records to fetch.
        Returns:
            list: A list of key metrics records.
        """
        self._validate_symbol(symbol)
        self._validate_period(period)
        self._validate_limit(limit)

        key_metrics = self.__get_by_url(
            endpoint="key-metrics",
            params={"symbol": symbol, "period": period, "limit": limit},
        )
        return self._handle_list_response(key_metrics, FMPKeyMetrics)

    def get_financial_ratios(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> list[FMPFinancialRatios]:
        """Fetches financial ratios for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the financial ratios for.
            period (str): The period for the financial ratios ('Q1','Q2','Q3','Q4','FY','annual','quarter').
            limit (int): The maximum number of records to fetch.
        Returns:
            list: A list of financial ratios records.
        """
        self._validate_symbol(symbol)
        self._validate_period(period)
        self._validate_limit(limit)

        ratios = self.__get_by_url(
            endpoint="ratios",
            params={"symbol": symbol, "period": period, "limit": limit},
        )
        return self._handle_list_response(ratios, FMPFinancialRatios)

    def get_financial_scores(self, symbol: str) -> Optional[FMPFinancialScores]:
        """Fetches financial scores for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the financial scores for.
        Returns:
            Optional[FMPFinancialScores]: The financial scores if found, else None.
        """
        self._validate_symbol(symbol)
        data = self.__get_by_url(endpoint="financial-scores", params={"symbol": symbol})
        return self._handle_single_response(data, FMPFinancialScores)

    def get_company_gradings(self, symbol: str) -> list[FMPStockGrading]:
        """Fetches stock grading history for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the grading history for.
        Returns:
            list: A list of stock grading records.
        """
        grades = self.__get_by_url(endpoint="grades", params={"symbol": symbol})
        return self._handle_list_response(grades, FMPStockGrading)

    def get_company_grading_summary(self, symbol: str) -> FMPStockGradingSummary | None:
        """Fetches stock grading summary for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the grading summary for.
        Returns:
            Optional[FMPStockGradingSummary]: The stock grading summary if found, else None.
        """
        summary = self.__get_by_url(
            endpoint="grades-consensus", params={"symbol": symbol}
        )
        return self._handle_single_response(summary, FMPStockGradingSummary)

    def get_stock_peer_companies(self, symbol: str) -> list[FMPStockPeer]:
        """Fetches peer companies for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the peer companies for.
        Returns:
            list: A list of peer company profiles.
        """
        peers = self.__get_by_url(endpoint="stock-peers", params={"symbol": symbol})
        return self._handle_list_response(peers, FMPStockPeer)

    def get_price_target_news(
        self, symbol: str, page: int = 1, limit: int = 10
    ) -> list[FMPPriceTargetNews]:
        """Fetches news related to stock price targets for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the price target news for.
            page (int): The page number to fetch.
            limit (int): The maximum number of news records to fetch.
        Returns:
            list: A list of price target news records.
        """
        price_target_news = self.__get_by_url(
            endpoint="price-target-news",
            params={"symbol": symbol, "limit": limit, "page": page},
        )
        return self._handle_list_response(price_target_news, FMPPriceTargetNews)

    def get_grading_news(
        self, symbol: str, limit: int = 100
    ) -> list[FMPStockGradingNews]:
        """Fetches news related to stock grading changes for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the grading news for.
            limit (int): The maximum number of news records to fetch.
        Returns:
            list: A list of stock grading news records.
        """
        news = self.__get_by_url(
            endpoint="grades-news", params={"symbol": symbol, "limit": limit}
        )
        return self._handle_list_response(news, FMPStockGradingNews)

    # news
    def get_latest_general_news(
        self, from_date: str, to_date: str, limit: int = 100, page: int = 0
    ) -> list[FMPGeneralNews]:
        """Fetches the latest general news articles with pagination.
        Args:
            page (int): The page number to fetch.
            limit (int): The maximum number of articles to fetch.
        Returns:
            list: A list of general news articles.
        """
        limit = min(limit, 100)  # maximum limit is 100
        general_news = self.__get_by_url(
            endpoint="news/general-latest",
            params={"page": page, "limit": limit, "from": from_date, "to": to_date},
        )
        return self._handle_list_response(general_news, FMPGeneralNews)

    def get_stock_news(
        self,
        symbol: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        limit: int = 20,
    ) -> list[FMPStockNews]:
        """Fetches stock-specific news articles for given stock symbols within a date range.
        Args:
            symbol (str): The stock symbol to fetch the news for.
            from_date (Optional[str]): The start date for the news in 'YYYY-MM-DD' format.
            to_date (Optional[str]): The end date for the news in 'YYYY-MM-DD' format.
            page (int): The page number to fetch.
            limit (int): The number of articles per page (maximum 100).
        Returns:
            list: A list of stock-specific news articles.
        """
        if page < 1:
            raise ValueError("Page number must be greater than 0.")
        limit = min(limit, 100)  # maximum limit is 100
        stock_news = self.__get_by_url(
            endpoint="news/stock",
            params={
                "symbols": symbol,
                "from": from_date,
                "to": to_date,
                "page": page,
                "limit": limit,
            },
        )
        return self._handle_list_response(stock_news, FMPStockNews)

    def get_price_target(self, symbol: str) -> FMPStockPriceTarget | None:
        """Fetches stock price target for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the price target for.
        Returns:
            Optional[FMPStockPriceTarget]: The stock price target if found, else None.
        """
        price_target = self.__get_by_url(
            endpoint="price-target-consensus", params={"symbol": symbol}
        )
        return self._handle_single_response(price_target, FMPStockPriceTarget)

    def get_price_target_summary(
        self, symbol: str
    ) -> FMPStockPriceTargetSummary | None:
        """Fetches stock price target summary for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the price target summary for.
        Returns:
            Optional[FMPStockPriceTargetSummary]: The stock price target summary if found, else None
        """
        price_target = self.__get_by_url(
            endpoint="price-target-summary", params={"symbol": symbol}
        )
        return self._handle_single_response(price_target, FMPStockPriceTargetSummary)

    def get_company_rating(self, symbol: str) -> FMPStockRating | None:
        """Fetches stock rating for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the rating for.
        Returns:
            Optional[FMPStockRating]: The stock rating if found, else None.
        """
        rating = self.__get_by_url(
            endpoint="ratings-snapshot", params={"symbol": symbol}
        )
        return self._handle_single_response(rating, FMPStockRating)

    def get_dividends(self, symbol: str, limit: int = 100) -> list[FMPDividend]:
        """Fetches the dividend history for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the dividends for.
        Returns:
            list: A list of dividend records.
        """
        historical_dividends = self.__get_by_url(
            endpoint="dividends",
            params={"symbol": symbol, "limit": limit},
        )
        return self._handle_list_response(historical_dividends, FMPDividend)

    def get_dividend_calendar(
        self, from_date: Optional[str] = None, to_date: Optional[str] = None
    ) -> list[FMPDividendCalendar]:
        """Fetches the dividend calendar within a specified date range.
        maximum range is 90 days.
        Args:
            from_date (Optional[str]): The start date for the calendar in 'YYYY-MM-DD' format.
            to_date (Optional[str]): The end date for the calendar in 'YYYY-MM-DD' format.
        Returns:
            list: A list of dividend records within the specified date range.
        """
        if IS_DEV:
            params = {}
        else:
            params = {"from": from_date, "to": to_date}
        calendar = self.__get_by_url(
            endpoint="dividends-calendar",
            params=params,
        )
        return self._handle_list_response(calendar, FMPDividendCalendar)

    def get_stock_splits(self, symbol: str) -> list[FMPStockSplit]:
        """Fetches the stock split history for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the stock splits for.
        Returns:
            list: A list of stock split records.
        """
        historical_splits = self.__get_by_url(
            endpoint="splits",
            params={"symbol": symbol},
        )
        return self._handle_list_response(historical_splits, FMPStockSplit)

    def get_analyst_estimates(
        self, symbol: str, period: str = "quarter", limit: int = 10
    ) -> list[FMPAnalystEstimates]:
        """Fetches analyst estimates for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the estimates for.
            period (str): The period for the estimates ('quarter' or 'annual').
            limit (int): The maximum number of records to fetch.
        Returns:
            list: A list of analyst estimates.
        """
        if IS_DEV:
            params = {"symbol": symbol, "period": "annual"}
        else:
            params = {"symbol": symbol, "period": period, "limit": limit}
        estimates = self.__get_by_url(
            endpoint="analyst-estimates",
            params=params,
        )
        return self._handle_list_response(estimates, FMPAnalystEstimates)

    def get_revenue_product_segmentation(
        self,
        symbol: str,
        period: str = "annual",
    ) -> list[FMPRevenueProductSegmentation]:
        """Fetches revenue product segmentation for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the data for.
            period (int): The period to fetch the data for.
        Returns:
            list: A list of revenue product segmentation records.
        """
        data = self.__get_by_url(
            endpoint="revenue-product-segmentation",
            params={"symbol": symbol, "period": period},
        )
        return self._handle_list_response(data, FMPRevenueProductSegmentation)

    def get_discounted_cash_flow(self, symbol: str) -> FMPDFCValuation | None:
        """Fetches the discounted cash flow valuation for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the DCF valuation for.
        Returns:
            Optional[FMPDFCValuation]: The DCF valuation if found, else None.
        """
        dfc = self.__get_by_url(
            endpoint="discounted-cash-flow", params={"symbol": symbol}
        )
        return self._handle_single_response(dfc, FMPDFCValuation)

    def get_levered_discounted_cash_flow(
        self, symbol: str
    ) -> Optional[FMPDFCValuation]:
        """Fetches the levered discounted cash flow valuation for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the levered DCF valuation for.
        Returns:
            Optional[FMPDFCValuation]: The levered DCF valuation if found, else None.
        """
        dfc = self.__get_by_url(
            endpoint="levered-discounted-cash-flow", params={"symbol": symbol}
        )
        return self._handle_single_response(dfc, FMPDFCValuation)

    def get_custom_discounted_cash_flow(
        self, symbol: str, params: Dict[str, Any]
    ) -> Optional[FMPDFCValuation]:
        """Fetches the discounted cash flow valuation for a given stock symbol with custom parameters.
        Args:
            symbol (str): The stock symbol to fetch the DCF valuation for.
            params (Dict[str, Any]): A dictionary of custom parameters for the DCF calculation.
        Returns:
            Optional[FMPDFCValuation]: The DCF valuation if found, else None.
        """
        dfc = self.__get_by_url(
            endpoint="custom-discounted-cash-flow", params={"symbol": symbol, **params}
        )
        return self._handle_single_response(dfc, FMPDFCValuation)

    def get_price_change_quote(self, symbol: str) -> Optional[FMPStockPriceChange]:
        """Fetches the price change quote for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the price change quote for.
        Returns:
            Optional[FMPStockPriceChange]: The price change quote if found, else None.
        """
        price_change = self.__get_by_url(
            endpoint="stock-price-change", params={"symbol": symbol}
        )
        return self._handle_single_response(price_change, FMPStockPriceChange)

    def get_current_price_quote(self, symbol: str) -> Optional[FMPStockPrice]:
        """Fetches the current price quote for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the current price quote for.
        Returns:
            Optional[FMPStockPrice]: The current price quote if found, else None.
        """
        current_price = self.__get_by_url(endpoint="quote", params={"symbol": symbol})
        return self._handle_single_response(current_price, FMPStockPrice)

    def get_after_hours_price(self, symbol: str) -> Optional[FMPAfterHoursPrice]:
        """Fetches the after-hours price for a given stock symbol.
        Args:
            symbol (str): The stock symbol to fetch the after-hours price for.
        Returns:
            Optional[FMPAfterHoursPrice]: The after-hours price if found, else None.
        """
        after_hours_price = self.__get_by_url(
            endpoint="aftermarket-trade", params={"symbol": symbol}
        )
        return self._handle_single_response(after_hours_price, FMPAfterHoursPrice)

    def get_historical_prices(
        self, symbol: str, from_date: str, to_date: str
    ) -> list[FMPStockPrice]:
        """Fetches historical stock prices for a given stock symbol within a date range.
        Args:
            symbol (str): The stock symbol to fetch the historical prices for.
            from_date (str): The start date for the historical prices in 'YYYY-MM-DD' format.
            to_date (str): The end date for the historical prices in 'YYYY-MM-DD' format.
        Returns:
            list: A list of historical stock price records within the specified date range.
        """
        historical_prices = self.__get_by_url(
            endpoint="historical-price-eod/full",
            params={"symbol": symbol, "from": from_date, "to": to_date},
        )
        historical_prices = self._handle_list_response(
            historical_prices, FMPStockHistoricalPrice
        )
        return [
            FMPStockPrice(
                **{
                    "symbol": price.symbol,
                    "date": price.date,
                    "open_price": price.open,
                    "high_price": price.high,
                    "low_price": price.low,
                    "close_price": price.close,
                    "volume": price.volume,
                    "change": price.change,
                    "change_percent": price.change_percent,
                }
            )
            for price in historical_prices
        ]

    def _validate_symbol(self, symbol: str) -> None:
        """Validate stock symbol parameter"""
        if not symbol or not symbol.strip():
            raise ValueError("Symbol cannot be empty")

    def _validate_period(self, period: str) -> None:
        """Validate period parameter"""
        if period not in PERIODS:
            raise ValueError(f"Period must be one of: {', '.join(PERIODS)}")

    def _validate_limit(self, limit: int) -> None:
        """Validate limit parameter"""
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

    def _handle_list_response(self, data: Any, model_class) -> list:
        """Standardized handling of list responses"""
        if not data:
            return []
        if not isinstance(data, list):
            logger.warning(f"Expected list response, got {type(data)}")
            return []
        try:
            return [model_class(**item) for item in data]
        except Exception as e:
            logger.error(f"Error parsing response data: {e}")
            return []

    def _handle_single_response(self, data: Any, model_class) -> Optional[Any]:
        """Standardized handling of single item responses"""
        if not data:
            return None
        try:
            if isinstance(data, list) and len(data) > 0:
                return model_class(**data[0])
            elif isinstance(data, dict):
                return model_class(**data)
        except Exception as e:
            logger.error(f"Error parsing response data: {e}")
        return None

    def _apply_rate_limiting(self) -> None:
        """Apply rate limiting to prevent API throttling"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.config.rate_limit_delay:
            sleep_time = self.config.rate_limit_delay - time_since_last_request
            time.sleep(sleep_time)
        self._last_request_time = time.time()

    def __get_by_url(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict]:
        """Helper method to perform GET requests to the FMP API.
        Args:
            endpoint (str): The API endpoint to call.
            params (Optional[Dict[str, Any]]): Additional query parameters.
        Returns:
            Optional[Dict]: The JSON response from the API if successful, else None.
        """
        if params is None:
            params = {}
        params["apikey"] = self.token

        internal_url = f"{self.BASE_URL}/{endpoint}"

        # Apply rate limiting
        self._apply_rate_limiting()

        for attempt in range(self.config.max_retries):
            try:
                response = requests.get(
                    internal_url, params=params, timeout=self.timeout
                )
                response.raise_for_status()

                data = response.json()

                # Validate response structure
                if not data:
                    logger.warning(f"Empty response from {endpoint}")
                    return None

                # Check for API-specific error messages
                if isinstance(data, dict) and "Error Message" in data:
                    logger.error(f"API error from {endpoint}: {data['Error Message']}")
                    raise FMPError(data["Error Message"])

                return data

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout calling {endpoint} (attempt {attempt + 1})")
                if attempt == self.config.max_retries - 1:
                    raise FMPTimeoutError(f"Request timeout for {endpoint}")

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    # Rate limit exceeded
                    if attempt == self.config.max_retries - 1:
                        raise FMPRateLimitError("API rate limit exceeded")
                    wait_time = self.config.backoff_factor * (2**attempt)
                    logger.warning(f"Rate limit exceeded. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(
                        f"HTTP error {e.response.status_code} calling {endpoint}: {e}"
                    )
                    raise FMPHTTPError(f"HTTP {e.response.status_code}: {e}")

            except ValueError as e:  # JSON decode error
                logger.error(f"Invalid JSON response from {endpoint}: {e}")
                raise FMPError(f"Invalid JSON response: {e}")

            except requests.RequestException as e:
                logger.error(
                    f"Request failed for {endpoint} (attempt {attempt + 1}): {e}"
                )
                if attempt == self.config.max_retries - 1:
                    raise FMPConnectionError(f"Failed to connect to {endpoint}: {e}")

        return None
