from typing import Any, Dict, List, Optional, Protocol

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
from app.clients.fmp.models.quotes import FMPStockPrice, FMPStockPriceChange
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


class FMPClientProtocol(Protocol):
    """Protocol defining the interface for FMP API clients."""

    # Stock Screening
    def get_stock_screeners(self, params: Dict[str, Any]) -> List[FMPStockScreenResult]:
        """Fetches stock screener results based on provided parameters."""
        ...

    # Company Information
    def get_company_profile(self, symbol: str) -> Optional[FMPCompanyProfile]:
        """Fetches the company profile for a given stock symbol."""
        ...

    # Financial Statements
    def get_income_statements(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[FMPCompanyIncomeStatement]:
        """Fetches the income statement for a given stock symbol."""
        ...

    def get_balance_sheets(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[FMPCompanyBalanceSheet]:
        """Fetches the balance sheet for a given stock symbol."""
        ...

    def get_cash_flow_statements(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[FMPCompanyCashFlowStatement]:
        """Fetches the cash flow statement for a given stock symbol."""
        ...

    # Financial Metrics
    def get_key_metrics(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[FMPKeyMetrics]:
        """Fetches key metrics for a given stock symbol."""
        ...

    def get_financial_ratios(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[FMPFinancialRatios]:
        """Fetches financial ratios for a given stock symbol."""
        ...

    def get_financial_scores(self, symbol: str) -> Optional[FMPFinancialScores]:
        """Fetches financial scores for a given stock symbol."""
        ...

    # Stock Analysis
    def get_company_gradings(self, symbol: str) -> List[FMPStockGrading]:
        """Fetches stock grading history for a given stock symbol."""
        ...

    def get_company_grading_summary(
        self, symbol: str
    ) -> Optional[FMPStockGradingSummary]:
        """Fetches stock grading summary for a given stock symbol."""
        ...

    def get_stock_peer_companies(self, symbol: str) -> List[FMPStockPeer]:
        """Fetches peer companies for a given stock symbol."""
        ...

    def get_company_rating(self, symbol: str) -> Optional[FMPStockRating]:
        """Fetches stock rating for a given stock symbol."""
        ...

    # Price Targets
    def get_price_target(self, symbol: str) -> Optional[FMPStockPriceTarget]:
        """Fetches stock price target for a given stock symbol."""
        ...

    def get_price_target_summary(
        self, symbol: str
    ) -> Optional[FMPStockPriceTargetSummary]:
        """Fetches stock price target summary for a given stock symbol."""
        ...

    # News
    def get_price_target_news(
        self, symbol: str, page: int = 1, limit: int = 10
    ) -> List[FMPPriceTargetNews]:
        """Fetches news related to stock price targets for a given stock symbol."""
        ...

    def get_grading_news(
        self, symbol: str, limit: int = 100
    ) -> List[FMPStockGradingNews]:
        """Fetches news related to stock grading changes for a given stock symbol."""
        ...

    def get_latest_general_news(
        self, from_date: str, to_date: str, limit: int = 100, page: int = 0
    ) -> List[FMPGeneralNews]:
        """Fetches the latest general news articles with pagination."""
        ...

    def get_stock_news(
        self,
        symbol: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        limit: int = 20,
    ) -> List[FMPStockNews]:
        """Fetches stock-specific news articles for given stock symbols within a date range."""
        ...

    # Dividends and Splits
    def get_dividends(self, symbol: str, limit: int = 100) -> List[FMPDividend]:
        """Fetches the dividend history for a given stock symbol."""
        ...

    def get_dividend_calendar(
        self, from_date: Optional[str] = None, to_date: Optional[str] = None
    ) -> List[FMPDividendCalendar]:
        """Fetches the dividend calendar within a specified date range."""
        ...

    def get_stock_splits(self, symbol: str) -> List[FMPStockSplit]:
        """Fetches the stock split history for a given stock symbol."""
        ...

    # Analyst Data
    def get_analyst_estimates(
        self, symbol: str, period: str = "quarter", limit: int = 10
    ) -> List[FMPAnalystEstimates]:
        """Fetches analyst estimates for a given stock symbol."""
        ...

    def get_revenue_product_segmentation(
        self,
        symbol: str,
        period: str = "annual",
    ) -> List[FMPRevenueProductSegmentation]:
        """Fetches revenue product segmentation for a given stock symbol."""
        ...

    # Valuation
    def get_discounted_cash_flow(self, symbol: str) -> Optional[FMPDFCValuation]:
        """Fetches the discounted cash flow valuation for a given stock symbol."""
        ...

    def get_levered_discounted_cash_flow(
        self, symbol: str
    ) -> Optional[FMPDFCValuation]:
        """Fetches the levered discounted cash flow valuation for a given stock symbol."""
        ...

    def get_custom_discounted_cash_flow(
        self, symbol: str, params: Dict[str, Any]
    ) -> Optional[FMPDFCValuation]:
        """Fetches the discounted cash flow valuation for a given stock symbol with custom parameters."""
        ...

    def get_price_change_quote(self, symbol: str) -> Optional[FMPStockPriceChange]:
        """Fetches the stock price change quote for a given stock symbol."""
        ...

    def get_current_price_quote(self, symbol: str) -> Optional[FMPStockPrice]:
        """Fetches the current stock price quote for a given stock symbol."""
        ...
