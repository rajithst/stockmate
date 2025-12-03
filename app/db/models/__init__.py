from app.db.engine import Base  # Ensure Base is imported before schemas

# Financial Statement Models
from .financial_statements import (
    CompanyIncomeStatement,
    CompanyBalanceSheet,
    CompanyCashFlowStatement,
    CompanyFinancialRatio,
)

# Company Metrics Models
from .company_metrics import (
    CompanyAnalystEstimate,
    CompanyKeyMetrics,
    CompanyDiscountedCashFlow,
    CompanyRevenueProductSegmentation,
)

# Core Models
from .company import Company, NonUSCompany
from .dividend import CompanyDividend
from .financial_score import CompanyFinancialScore

# Market Data Models
from .grading import CompanyGrading, CompanyGradingSummary
from .news import (
    CompanyGeneralNews,
    CompanyGradingNews,
    CompanyPriceTargetNews,
    CompanyStockNews,
)
from .ratings import CompanyRatingSummary
from .stock import CompanyStockPeer, CompanyStockSplit
from .price_target import CompanyPriceTarget, CompanyPriceTargetSummary
from .quote import CompanyStockPriceChange, CompanyStockPrice, IndexQuote

# User/Portfolio Models
from .financial_health import CompanyFinancialHealth
from .technical_indicators import CompanyTechnicalIndicator
from .user import User, NotificationPreference
from .watchlist import Watchlist, WatchlistItem
from .portfolio import (
    Portfolio,
    PortfolioHoldingPerformance,
    PortfolioTradingHistory,
    PortfolioDividendHistory,
)

# Notification Models
from .notification import Notification

# Earnings Models
from .earnings import CompanyEarningsCalendar