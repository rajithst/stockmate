from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# Portfolio Schemas
class Portfolio(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    currency: str = "USD"
    total_value: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0
    dividends_received: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class PortfolioWrite(Portfolio):
    model_config = ConfigDict(from_attributes=True)


class PortfolioRead(Portfolio):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Portfolio Sector Performance Schemas
class PortfolioSectorPerformance(BaseModel):
    portfolio_id: int
    sector: str
    allocation_percentage: float = 0.0
    currency: str = "USD"
    total_invested: float = 0.0
    total_gain_loss: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class PortfolioSectorPerformanceWrite(PortfolioSectorPerformance):
    model_config = ConfigDict(from_attributes=True)


class PortfolioSectorPerformanceRead(PortfolioSectorPerformance):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Portfolio Industry Performance Schemas
class PortfolioIndustryPerformance(BaseModel):
    portfolio_id: int
    industry: str
    allocation_percentage: float = 0.0
    currency: str = "USD"
    total_invested: float = 0.0
    total_gain_loss: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class PortfolioIndustryPerformanceWrite(PortfolioIndustryPerformance):
    model_config = ConfigDict(from_attributes=True)


class PortfolioIndustryPerformanceRead(PortfolioIndustryPerformance):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Portfolio Holding Performance Schemas
class PortfolioHoldingPerformance(BaseModel):
    portfolio_id: int
    holding_symbol: str
    currency: str = "USD"
    total_shares: float = 0.0
    allocation_percentage: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class PortfolioHoldingPerformanceWrite(PortfolioHoldingPerformance):
    model_config = ConfigDict(from_attributes=True)


class PortfolioHoldingPerformanceRead(PortfolioHoldingPerformance):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Portfolio Trading History Schemas
class PortfolioTradingHistory(BaseModel):
    portfolio_id: int
    trade_type: str  # BUY or SELL
    currency: str = "USD"
    symbol: str
    shares: float = 0.0
    price_per_share: float = 0.0
    total_value: float = 0.0
    trade_date: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioTradingHistoryWrite(PortfolioTradingHistory):
    model_config = ConfigDict(from_attributes=True)


class PortfolioTradingHistoryRead(PortfolioTradingHistory):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Portfolio Dividend History Schemas
class PortfolioDividendHistory(BaseModel):
    portfolio_id: int
    symbol: str
    shares: float = 0.0
    dividend_per_share: float = 0.0
    dividend_amount: float = 0.0
    declaration_date: datetime
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioDividendHistoryWrite(PortfolioDividendHistory):
    model_config = ConfigDict(from_attributes=True)


class PortfolioDividendHistoryRead(PortfolioDividendHistory):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Composite Response Schemas
class PortfolioDetailRead(PortfolioRead):
    sector_performances: List[PortfolioSectorPerformanceRead] = []
    industry_performances: List[PortfolioIndustryPerformanceRead] = []
    holding_performances: List[PortfolioHoldingPerformanceRead] = []
    trading_histories: List[PortfolioTradingHistoryRead] = []
    dividend_histories: List[PortfolioDividendHistoryRead] = []

    model_config = ConfigDict(from_attributes=True)
