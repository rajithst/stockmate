from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# Portfolio Schemas
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
    total_value: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0
    dividends_received: float = 0.0
    total_return_percentage: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PortfolioUpdate(Portfolio):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


# Portfolio Sector Performance Schemas
class PortfolioSectorPerformance(BaseModel):
    sector: str
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)


class PortfolioSectorPerformanceRead(PortfolioSectorPerformance):
    allocation_percentage: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0

    model_config = ConfigDict(from_attributes=True)


# Portfolio Industry Performance Schemas
class PortfolioIndustryPerformance(BaseModel):
    industry: str
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)


class PortfolioIndustryPerformanceRead(PortfolioIndustryPerformance):
    allocation_percentage: float = 0.0
    total_invested: float = 0.0
    total_gain_loss: float = 0.0

    model_config = ConfigDict(from_attributes=True)


# Portfolio Holding Performance Schemas
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


# Portfolio Trading History Schemas
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


# Portfolio Dividend History Schemas
class PortfolioDividendHistory(BaseModel):
    symbol: str
    shares: float = 0.0
    dividend_per_share: float = 0.0
    dividend_amount: float = 0.0
    currency: str
    declaration_date: datetime
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioDividendHistoryRead(PortfolioDividendHistory):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Composite Response Schemas
class PortfolioDetail(BaseModel):
    portfolio: PortfolioRead
    sector_performances: List[PortfolioSectorPerformanceRead] = []
    industry_performances: List[PortfolioIndustryPerformanceRead] = []
    holding_performances: List[PortfolioHoldingPerformanceRead] = []
    trading_histories: List[PortfolioTradingHistoryRead] = []
    dividend_histories: List[PortfolioDividendHistoryRead] = []

    model_config = ConfigDict(from_attributes=True)
