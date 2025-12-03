from typing import List, Optional, Protocol

from app.clients.yfinance.models.company import (
    YFinanceCompanyProfile,
    YFinanceDividend,
)
from app.clients.yfinance.models.financial_statements import (
    YFinanceIncomeStatement,
    YFinanceBalanceSheet,
    YFinanceCashFlow,
)


class YFinanceClientProtocol(Protocol):
    """Protocol defining the interface for yfinance API clients."""

    # Company Information
    def get_company_profile(self, symbol: str) -> Optional[YFinanceCompanyProfile]:
        """Fetches company information for a given stock symbol."""
        ...

    # Financial Statements
    def get_income_statements(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[YFinanceIncomeStatement]:
        """Fetches the income statement for a given stock symbol."""
        ...

    def get_balance_sheets(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[YFinanceBalanceSheet]:
        """Fetches the balance sheet for a given stock symbol."""
        ...

    def get_cash_flow_statements(
        self, symbol: str, period: str = "annual", limit: int = 5
    ) -> List[YFinanceCashFlow]:
        """Fetches the cash flow statement for a given stock symbol."""
        ...

    def get_dividends(self, symbol: str, limit: int = 100) -> List[YFinanceDividend]:
        """Fetches the dividend history for a given stock symbol."""
        ...
