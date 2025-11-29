"""
Consolidated user and portfolio schemas:
- User: User account information
- NotificationPreference: User notification preferences
- Portfolio: Portfolio container and metadata
- PortfolioHoldingPerformance: Individual holdings and their performance
- PortfolioTradingHistory: Trade records and history
- PortfolioDividendHistory: Dividend records and history
- Watchlist: Watchlist container
- WatchlistItem: Items in watchlist
- Token: Authentication token
"""

from datetime import datetime, date as date_type
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.quote import (
    IndexQuoteRead,
    CompanyEarningsCalendarRead,
    CompanyDividendRead,
)


# ========================
# USER & AUTH SCHEMAS
# ========================


class User(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool = True
    last_login: Optional[datetime] = None
    last_password_change: Optional[datetime] = None
    theme_preference: str = "light"
    language_preference: str = "en"
    email_verified: bool = False
    two_factor_enabled: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Schema for user registration."""

    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Login request with username and password."""

    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserWrite(User):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(User):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ========================
# NOTIFICATION PREFERENCE SCHEMAS
# ========================


class NotificationPreference(BaseModel):
    user_id: int
    email_notifications: bool = True
    push_notifications: bool = False
    portfolio_alerts: bool = True
    price_alerts: bool = True
    daily_news_digest: bool = True
    weekly_report: bool = True

    model_config = ConfigDict(from_attributes=True)


class NotificationPreferenceWrite(NotificationPreference):
    model_config = ConfigDict(from_attributes=True)


class NotificationPreferenceRead(NotificationPreference):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# PORTFOLIO SCHEMAS
# ========================


class Portfolio(BaseModel):
    name: str
    description: Optional[str] = None
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)


class PortfolioUpsertRequest(Portfolio):
    model_config = ConfigDict(from_attributes=True)


class PortfolioCreate(Portfolio):
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class PortfolioRead(Portfolio):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PortfolioUpdate(Portfolio):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class PortfolioMonthlyPerformance(BaseModel):
    """Monthly portfolio performance data for charting."""

    year: int
    month: int
    date: date_type  # First day of the month
    total_value: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0
    gain_loss_percentage: float = 0.0
    dividends_received: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class PortfolioMonthlyPerformanceRead(PortfolioMonthlyPerformance):
    """Read schema for monthly performance with all calculated metrics."""

    model_config = ConfigDict(from_attributes=True)


# ========================
# PORTFOLIO SECTOR & INDUSTRY PERFORMANCE SCHEMAS
# ========================


class PortfolioSectorPerformance(BaseModel):
    sector: str
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)


class PortfolioSectorPerformanceRead(PortfolioSectorPerformance):
    allocation_percentage: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class PortfolioIndustryPerformance(BaseModel):
    industry: str
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)


class PortfolioIndustryPerformanceRead(PortfolioIndustryPerformance):
    allocation_percentage: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0

    model_config = ConfigDict(from_attributes=True)


# ========================
# PORTFOLIO HOLDING PERFORMANCE SCHEMAS
# ========================


class PortfolioHoldingPerformance(BaseModel):
    symbol: str
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)


class PortfolioHoldingPerformanceWrite(PortfolioHoldingPerformance):
    portfolio_id: int

    model_config = ConfigDict(from_attributes=True)


class PortfolioHoldingPerformanceRead(PortfolioHoldingPerformance):
    total_shares: float = 0.0
    total_invested: float = 0.0
    current_value: float = 0.0
    realized_gain_loss: float = 0.0
    unrealized_gain_loss: float = 0.0
    total_gain_loss: float = 0.0
    gain_loss_percentage: float = 0.0
    average_cost_per_share: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# PORTFOLIO TRADING HISTORY SCHEMAS
# ========================


class PortfolioTradingHistory(BaseModel):
    trade_type: str
    currency: str = "USD"
    symbol: str
    shares: float
    price_per_share: float
    total_value: float
    commission: float
    fees: float
    tax: float
    net_total: float
    trade_date: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioTradingHistoryUpsertRequest(PortfolioTradingHistory):
    model_config = ConfigDict(from_attributes=True)


class PortfolioTradingHistoryWrite(PortfolioTradingHistory):
    portfolio_id: int

    model_config = ConfigDict(from_attributes=True)


class PortfolioTradingHistoryRead(PortfolioTradingHistory):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# PORTFOLIO DIVIDEND HISTORY SCHEMAS
# ========================


class PortfolioDividendHistory(BaseModel):
    symbol: str
    shares: float = 0.0
    dividend_per_share: float = 0.0
    dividend_amount: float = 0.0
    currency: str
    declaration_date: date_type
    payment_date: date_type

    model_config = ConfigDict(from_attributes=True)


class PortfolioDividendHistoryRead(PortfolioDividendHistory):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PortfolioDividendHistoryWrite(PortfolioDividendHistory):
    portfolio_id: int

    model_config = ConfigDict(from_attributes=True)


# Composite Response Schemas
class PortfolioDetail(BaseModel):
    total_value: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0
    dividends_received: float = 0.0
    total_return_percentage: float = 0.0
    sector_performances: List[PortfolioSectorPerformanceRead] = []
    industry_performances: List[PortfolioIndustryPerformanceRead] = []
    holding_performances: List[PortfolioHoldingPerformanceRead] = []
    trading_histories: List[PortfolioTradingHistoryRead] = []
    monthly_performances: List[PortfolioMonthlyPerformanceRead] = []

    model_config = ConfigDict(from_attributes=True)


# Dividend Sync Response Schemas
class DividendSyncResult(BaseModel):
    portfolio_id: int
    processed_count: int
    skipped_count: int
    total_dividend_amount: float
    processed_symbols: List[str] = []


class DividendSyncBatchResult(BaseModel):
    total_processed: int
    total_skipped: int
    total_dividend_amount: float
    portfolio_results: List[DividendSyncResult] = []


# ========================
# WATCHLIST SCHEMAS
# ========================


class Watchlist(BaseModel):
    name: str
    currency: str = "USD"
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WatchlistUpsertRequest(Watchlist):
    model_config = ConfigDict(from_attributes=True)


class WatchlistCreate(Watchlist):
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class WatchlistUpdate(Watchlist):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class WatchlistRead(Watchlist):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# WATCHLIST ITEM SCHEMAS
# ========================


class WatchlistItem(BaseModel):
    symbol: str

    model_config = ConfigDict(from_attributes=True)


class WatchlistItemWrite(WatchlistItem):
    model_config = ConfigDict(from_attributes=True)


class WatchlistItemCreate(WatchlistItem):
    watchlist_id: int
    model_config = ConfigDict(from_attributes=True)


class WatchlistCompanyItem(BaseModel):
    id: int
    symbol: str
    company_name: str
    price: float
    currency: str
    price_change: float
    price_change_percent: float
    market_cap: float
    price_to_earnings_ratio: Optional[float] = None
    price_to_earnings_growth_ratio: Optional[float] = None
    forward_price_to_earnings_growth_ratio: Optional[float] = None
    price_to_book_ratio: Optional[float] = None
    price_to_sales_ratio: Optional[float] = None
    price_to_free_cash_flow_ratio: Optional[float] = None
    price_to_operating_cash_flow_ratio: Optional[float] = None
    image: Optional[str] = None


class WatchlistResponse(BaseModel):
    watchlist: WatchlistRead
    items: list[WatchlistCompanyItem] = []

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    total_portfolios: int = 0
    total_invested: float = 0.0
    total_current_value: float = 0.0
    total_profit_loss: float = 0.0
    total_dividends: float = 0.0
    gain_loss_percentage: float = 0.0
    index_quotes: list[IndexQuoteRead] = []
    earnings_calendar: list[CompanyEarningsCalendarRead] = []
    dividends_calendar: list[CompanyDividendRead] = []

    model_config = ConfigDict(from_attributes=True)


class StockSymbol(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    currency: str
    image: Optional[str] = None
    is_in_db: bool = False

    model_config = ConfigDict(from_attributes=True)
