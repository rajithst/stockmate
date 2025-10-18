from typing import Any, Dict, List, Optional, Protocol

from app.clients.fmp.models.analyst_estimates import FMPAnalystEstimates
from app.clients.fmp.models.company import FMPCompanyProfile
from app.clients.fmp.models.discounted_cashflow import FMPDFCValuation
from app.clients.fmp.models.dividend import FMPDividend
from app.clients.fmp.models.earnings import FMPEarnings
from app.clients.fmp.models.financial_ratios import (
    FMPFinancialRatios,
    FMPFinancialScores,
    FMPKeyMetrics,
)
from app.clients.fmp.models.financial_statements import (
    FMPCompanyBalanceSheet,
    FMPCompanyIncomeStatement,
)
from app.clients.fmp.models.news import (
    FMPGeneralNews,
    FMPPriceTargetNews,
    FMPStockGradingNews,
)
from app.clients.fmp.models.stock import (
    FMPStockGrading,
    FMPStockGradingSummary,
    FMPStockPeer,
    FMPStockPriceTarget,
    FMPStockRating,
    FMPStockScreenResult,
    FMPStockSplit,
)


class FMPClientProtocol(Protocol):
    def get_company_profile(self, symbol: str) -> Optional[FMPCompanyProfile]: ...

    def get_stock_screeners(
        self, params: Dict[str, Any]
    ) -> List[FMPStockScreenResult]: ...

    def get_stock_peer_companies(self, symbol: str) -> List[FMPStockPeer]: ...

    def get_dividends(self, symbol: str) -> List[FMPDividend]: ...
    def get_market_dividend_calendar(
        self, from_date: Optional[str], to_date: Optional[str]
    ) -> List[FMPDividend]: ...

    def get_income_statement(
        self, symbol: str, period: str, limit: int
    ) -> List[FMPCompanyIncomeStatement]: ...
    def get_balance_sheet(
        self, symbol: str, period: str, limit: int
    ) -> List[FMPCompanyBalanceSheet]: ...
    def get_cash_flow(
        self, symbol: str, period: str, limit: int
    ) -> List[FMPCompanyBalanceSheet]: ...

    def get_key_metrics(
        self, symbol: str, period: str, limit: int
    ) -> List[FMPKeyMetrics]: ...
    def get_financial_ratios(
        self, symbol: str, period: str, limit: int
    ) -> List[FMPFinancialRatios]: ...
    def get_financial_scores(self, symbol: str) -> Optional[FMPFinancialScores]: ...

    def get_stock_split(self, symbol: str) -> List[FMPStockSplit]: ...
    def get_market_stock_split_calendar(
        self, from_date: Optional[str], to_date: Optional[str]
    ) -> List[FMPStockSplit]: ...

    def get_earnings_calendar(
        self, from_date: Optional[str], to_date: Optional[str]
    ) -> List[FMPEarnings]: ...
    def get_analyst_estimates(
        self, symbol: str, period: str, limit: int
    ) -> List[FMPAnalystEstimates]: ...

    def get_ratings(self, symbol: str) -> Optional[FMPStockRating]: ...
    def get_price_target(self, symbol: str) -> Optional[FMPStockPriceTarget]: ...
    def get_price_target_news(
        self, symbol: str, limit: int
    ) -> List[FMPPriceTargetNews]: ...

    def get_stock_grade(self, symbol: str) -> List[FMPStockGrading]: ...
    def get_stock_grade_summary(
        self, symbol: str
    ) -> Optional[FMPStockGradingSummary]: ...
    def get_stock_grade_news(
        self, symbol: str, limit: int
    ) -> List[FMPStockGradingNews]: ...

    def get_latest_general_news(self, page: int) -> List[FMPGeneralNews]: ...
    def get_stock_news(
        self,
        symbols: List[str],
        from_date: Optional[str],
        to_date: Optional[str],
        page: int,
        limit: int,
    ) -> List[FMPGeneralNews]: ...

    def get_discounted_cash_flow(self, symbol: str) -> Optional[FMPDFCValuation]: ...
    def get_custom_discounted_cash_flow(
        self, symbol: str, params: Dict[str, Any]
    ) -> Optional[FMPDFCValuation]: ...
