from typing import Optional, Dict, Any

import fmpsdk
import requests
from fmpsdk import dividend_calendar, key_metrics

from app.clients.fmp.models.analyst_estimates import AnalystEstimates
from app.clients.fmp.models.company import CompanyProfile
from app.clients.fmp.models.discounted_cashflow import DFCValuation
from app.clients.fmp.models.dividend import Dividend
from app.clients.fmp.models.earnings import Earnings
from app.clients.fmp.models.financial_ratios import KeyMetrics, FinancialRatios, FinancialScores
from app.clients.fmp.models.financial_statements import CompanyIncomeStatement, CompanyBalanceSheet
from app.clients.fmp.models.news import GeneralNews, PriceTargetNews, StockGradingNews
from app.clients.fmp.models.stock import StockSplit, StockPeer, StockScreenResult, StockRating, StockPriceTarget, \
    StockGrading, StockGradingSummary

BASE_URL = "https://financialmodelingprep.com/stable"

class FMPClient:
    def __init__(self, token):
        self.token = token
        self.BASE_URL = BASE_URL
        self.timeout = 10  # seconds

    def __get_by_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
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

        try:
            response = requests.get(internal_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[FMPClient] Error calling {endpoint}: {e}")
            return None

    def get_stock_screeners(self, params: Dict[str: any]) -> list[StockScreenResult]:
        """Fetches stock screener results based on provided parameters.
            Args:
                params (Dict[str, any]): A dictionary of screener parameters.
            Returns:
                list: A list of stock screener results.
        """
        screener_params = {
            'market_cap_more_than': params.get('market_cap_more_than'),
            'market_cap_lower_than': params.get('market_cap_lower_than'),
            'beta_more_than': params.get('beta_more_than'),
            'beta_lower_than': params.get('beta_lower_than'),
            'volume_more_than': params.get('volume_more_than'),
            'volume_lower_than': params.get('volume_lower_than'),
            'price_more_than': params.get('price_more_than'),
            'price_lower_than': params.get('price_lower_than'),
            'dividend_more_than': params.get('dividend_more_than'),
            'dividend_lower_than': params.get('dividend_lower_than'),
            'is_actively_trading': params.get('is_actively_trading'),
            'exchange': params.get('exchange'),
            'sector': params.get('sector'),
            'industry': params.get('industry'),
            'country': params.get('country'),
            'limit': params.get('limit', 10),
        }
        stocks = fmpsdk.stock_screener(**screener_params, apikey=self.token)
        return [StockScreenResult(**stock) for stock in stocks] if stocks else []

    def get_company_profile(self, symbol: str) -> Optional[CompanyProfile]:
        """Fetches the company profile for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the profile for.
            Returns:
                Optional[CompanyProfile]: The company profile if found, else None.
        """

        profile = fmpsdk.company_profile(symbol=symbol, apikey=self.token)
        if profile and isinstance(profile, list):
            return CompanyProfile(**profile[0])
        return None

    def get_stock_peer_companies(self, symbol: str) -> list[StockPeer]:
        """Fetches peer companies for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the peer companies for.
            Returns:
                list: A list of peer company profiles.
        """
        peers = fmpsdk.company_valuation.stock_peers(symbol=symbol, apikey=self.token)
        return [StockPeer(**peer) for peer in peers] if peers else []

    # dividends

    def get_dividends(self, symbol: str) -> list[Dividend]:
        """Fetches the dividend history for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the dividends for.
            Returns:
                list: A list of dividend records.
        """
        historical_dividends = fmpsdk.historical_stock_dividend(symbol=symbol, apikey=self.token)
        return [Dividend(**dividend) for dividend in historical_dividends] if historical_dividends else []

    def get_market_dividend_calendar(self, from_date: Optional[str] = None, to_date: Optional[str] = None) -> list[Dividend]:
        """Fetches the market dividend calendar within a specified date range.
        maximum range is 90 days.
        Args:
            from_date (Optional[str]): The start date for the calendar in 'YYYY-MM-DD' format.
            to_date (Optional[str]): The end date for the calendar in 'YYYY-MM-DD' format.
        Returns:
            list: A list of dividend records within the specified date range.
        """
        calendar = fmpsdk.dividend_calendar(from_date=from_date, to_date=to_date, apikey=self.token)
        return [Dividend(**dividend) for dividend in calendar] if dividend_calendar else []

    # financial statements
    def get_income_statement(self, symbol: str, period: str = 'annual', limit: int = 5) -> list[CompanyIncomeStatement]:
        """Fetches the income statement for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the income statement for.
                period (str): The period for the income statement ('quarter' or 'annual').
                limit (int): The maximum number of records to fetch.
            Returns:
                list: A list of income statement records.
        """
        if period not in ['quarter', 'annual']:
            raise ValueError("Period must be either 'quarter' or 'annual'.")
        if not symbol:
            raise ValueError("Symbol is required.")

        income_statements = fmpsdk.income_statement(symbol=symbol, period=period, limit=limit, apikey=self.token)
        return [CompanyIncomeStatement(**stmt) for stmt in income_statements] if income_statements else []

    def get_balance_sheet(self, symbol: str, period: str = 'annual', limit: int = 5) -> list[CompanyBalanceSheet]:
        """Fetches the balance sheet for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the balance sheet for.
                period (str): The period for the balance sheet ('quarter' or 'annual').
                limit (int): The maximum number of records to fetch.
            Returns:
                list: A list of balance sheet records.
        """
        if period not in ['quarter', 'annual']:
            raise ValueError("Period must be either 'quarter' or 'annual'.")
        if not symbol:
            raise ValueError("Symbol is required.")
        balance_sheets = fmpsdk.balance_sheet_statement(symbol=symbol, period=period, limit=limit, apikey=self.token)
        return [CompanyBalanceSheet(**stmt) for stmt in balance_sheets] if balance_sheets else []

    def get_cash_flow(self, symbol: str, period: str = 'annual', limit: int = 5) -> list[CompanyBalanceSheet]:
        """Fetches the cash flow statement for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the cash flow statement for.
                period (str): The period for the cash flow statement ('quarter' or 'annual').
                limit (int): The maximum number of records to fetch.
            Returns:
                list: A list of cash flow statement records.
        """
        if period not in ['quarter', 'annual']:
            raise ValueError("Period must be either 'quarter' or 'annual'.")
        if not symbol:
            raise ValueError("Symbol is required.")
        cash_flow_statements = fmpsdk.cash_flow_statement(symbol=symbol, period=period, limit=limit, apikey=self.token)
        return [CompanyBalanceSheet(**stmt) for stmt in cash_flow_statements] if cash_flow_statements else []

    def get_key_metrics(self, symbol: str, period: str = 'annual', limit: int = 5) -> list[KeyMetrics]:
        """Fetches key metrics for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the key metrics for.
                period (str): The period for the key metrics ('Q1','Q2','Q3','Q4','FY','annual','quarter').
                limit (int): The maximum number of records to fetch.
            Returns:
                list: A list of key metrics records.
        """
        if period not in ['Q1','Q2','Q3','Q4','FY','annual','quarter']:
            raise ValueError("Period must be either 'quarter' or 'annual'.")
        if not symbol:
            raise ValueError("Symbol is required.")
        key_metrics_data = fmpsdk.key_metrics(symbol=symbol, period=period, limit=limit, apikey=self.token)
        return [KeyMetrics(**metric) for metric in key_metrics_data] if key_metrics else []

    def get_financial_ratios(self, symbol: str, period: str = 'annual', limit: int = 5) -> list[FinancialRatios]:
        """Fetches financial ratios for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the financial ratios for.
                period (str): The period for the financial ratios ('Q1','Q2','Q3','Q4','FY','annual','quarter').
                limit (int): The maximum number of records to fetch.
            Returns:
                list: A list of financial ratios records.
        """
        if period not in ['Q1','Q2','Q3','Q4','FY','annual','quarter']:
            raise ValueError("Period must be either 'quarter' or 'annual'.")
        if not symbol:
            raise ValueError("Symbol is required.")
        ratios = fmpsdk.financial_ratios(symbol=symbol, period=period, limit=limit, apikey=self.token)
        return [FinancialRatios(**ratio) for ratio in ratios] if ratios else []

    def get_financial_scores(self, symbol: str) -> Optional[FinancialScores]:
        """Fetches financial scores for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the financial scores for.
            Returns:
                Optional[FinancialScores]: The financial scores if found, else None.
        """
        if not symbol:
            raise ValueError("Symbol is required.")
        data = self.__get_by_url(endpoint='financial-scores', params={"symbol": symbol})
        if data:
            return FinancialScores(**data[0])
        return None


    # stock splits

    def get_stock_split(self, symbol: str)  -> list[StockSplit]:
        """Fetches the stock split history for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the stock splits for.
            Returns:
                list: A list of stock split records.
        """
        historical_splits = fmpsdk.historical_stock_split(symbol=symbol, apikey=self.token)
        return [StockSplit(**split) for split in historical_splits] if historical_splits else []

    def get_market_stock_split_calendar(self, from_date: Optional[str] = None, to_date: Optional[str] = None) -> list[StockSplit]:
        """Fetches the market stock split calendar within a specified date range.
        maximum range is 90 days.
        Args:
            from_date (Optional[str]): The start date for the calendar in 'YYYY-MM-DD' format.
            to_date (Optional[str]): The end date for the calendar in 'YYYY-MM-DD' format.
        Returns:
            list: A list of stock split records within the specified date range.
        """
        calendar = fmpsdk.stock_split_calendar(from_date=from_date, to_date=to_date, apikey=self.token)
        return [StockSplit(**split) for split in calendar] if calendar else []

    # earnings
    def get_earnings_calendar(self, from_date: Optional[str] = None, to_date: Optional[str] = None) -> list[Earnings]:
        """Fetches the earnings calendar within a specified date range.
        maximum range is 90 days.
        Args:
            from_date (Optional[str]): The start date for the calendar in 'YYYY-MM-DD' format.
            to_date (Optional[str]): The end date for the calendar in 'YYYY-MM-DD' format.
        Returns:
            list: A list of earnings records within the specified date range.
        """
        earnings_calendar = fmpsdk.earning_calendar(from_date=from_date, to_date=to_date, apikey=self.token)
        return [Earnings(**earning) for earning in earnings_calendar] if earnings_calendar else []

    # analyst estimates
    def get_analyst_estimates(self, symbol: str, period: str = 'quarter', limit: int = 10) -> list[AnalystEstimates]:
        """Fetches analyst estimates for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the estimates for.
                period (str): The period for the estimates ('quarter' or 'annual').
                limit (int): The maximum number of records to fetch.
            Returns:
                list: A list of analyst estimates.
        """
        estimates = fmpsdk.company_valuation.analyst_estimates(symbol=symbol, period=period, limit=limit, apikey=self.token)
        return [AnalystEstimates(**estimate) for estimate in estimates] if estimates else []

    def get_ratings(self, symbol: str) -> Optional[StockRating]:
        """Fetches stock ratings for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the ratings for.
            Returns:
                Optional[StockRating]: The stock rating if found, else None.
        """
        ratings = fmpsdk.rating(symbol=symbol, apikey=self.token)
        if ratings:
            return StockRating(**ratings[0])
        return None

    def get_price_target(self, symbol: str) -> Optional[StockPriceTarget]:
        """Fetches stock price target for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the price target for.
            Returns:
                Optional[StockPriceTarget]: The stock price target if found, else None.
        """
        price_target = self.__get_by_url(endpoint='price-target', params={"symbol": symbol})
        if price_target:
            return StockPriceTarget(**price_target[0])
        return None

    def get_price_target_news(self, symbol: str, limit: int = 10) -> list[PriceTargetNews]:
        """Fetches news related to stock price targets for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the price target news for.
                limit (int): The maximum number of news records to fetch.
            Returns:
                list: A list of price target news records.
        """
        price_target_news = self.__get_by_url(endpoint='price-target-news', params={"symbol": symbol, "limit": limit})
        if price_target_news:
            return [PriceTargetNews(**news) for news in price_target_news]
        return []

    def get_stock_grade(self, symbol: str) -> list[StockGrading]:
        """Fetches stock grading history for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the grading history for.
            Returns:
                list: A list of stock grading records.
        """
        grades = self.__get_by_url(endpoint='grades', params={"symbol": symbol})
        if grades:
            return [StockGrading(**grade) for grade in grades]
        return []

    def get_stock_grade_summary(self, symbol: str) -> Optional[StockGradingSummary]:
        """Fetches stock grading summary for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the grading summary for.
            Returns:
                Optional[StockGradingSummary]: The stock grading summary if found, else None.
        """
        summary = self.__get_by_url(endpoint='grades-summary', params={"symbol": symbol})
        if summary:
            return summary and StockGradingSummary(**summary[0])
        return None

    def get_stock_grade_news(self, symbol: str, limit: int = 100) -> list[StockGradingNews]:
        """Fetches news related to stock grading changes for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the grading news for.
                limit (int): The maximum number of news records to fetch.
            Returns:
                list: A list of stock grading news records.
        """
        news = self.__get_by_url(endpoint='grades-news', params={"symbol": symbol, "limit": limit})
        if news:
            return [StockGradingNews(**grade) for grade in news]
        return []

    # news
    def get_latest_general_news(self, page: int = 0) -> list[GeneralNews]:
        """Fetches the latest general news articles with pagination.
            Args:
                page (int): The page number to fetch.
            Returns:
                list: A list of general news articles.
        """
        if page < 1:
            raise ValueError("Page number must be greater than 0.")
        general_news = fmpsdk.general_news(page=page, apikey=self.token)
        return [GeneralNews(**news) for news in general_news] if general_news else []

    def get_stock_news(self, symbols: list[str], from_date: Optional[str] = None, to_date: Optional[str] = None, page: int = 0, limit: int = 20) -> list[GeneralNews]:
        """Fetches stock-specific news articles within a specified date range and pagination.
            Args:
                symbols (list[str]): A list of stock symbols to fetch news for.
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
        stock_news = fmpsdk.stock_news(tickers=symbols, from_date=from_date, to_date=to_date, page=page, limit=limit, apikey=self.token)
        return [GeneralNews(**news) for news in stock_news] if stock_news else []


    # discounted cash flow
    def get_discounted_cash_flow(self, symbol: str) -> Optional[DFCValuation]:
        """Fetches the discounted cash flow valuation for a given stock symbol.
            Args:
                symbol (str): The stock symbol to fetch the DCF valuation for.
            Returns:
                Optional[DFCValuation]: The DCF valuation if found, else None.
        """
        dfc = fmpsdk.discounted_cash_flow(symbol=symbol, apikey=self.token)
        if dfc and isinstance(dfc, list):
            return DFCValuation(**dfc[0])
        return None

    def get_custom_discounted_cash_flow(self, symbol: str, params: Dict[str, Any]) -> Optional[DFCValuation]:
        """Fetches the discounted cash flow valuation for a given stock symbol with custom parameters.
            Args:
                symbol (str): The stock symbol to fetch the DCF valuation for.
                params (Dict[str, Any]): A dictionary of custom parameters for the DCF calculation.
            Returns:
                Optional[DFCValuation]: The DCF valuation if found, else None.
        """
        dfc = self.__get_by_url(endpoint='custom-discounted-cash-flow', params={"symbol": symbol, **params})
        if dfc and isinstance(dfc, list):
            return DFCValuation(**dfc[0])
        return None

