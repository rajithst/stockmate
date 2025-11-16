"""
Consolidated quote and technical data schemas:
- StockPrice/StockPriceChange: Daily price and change data
- CompanyStockSplit: Stock split records
- CompanyStockPeer: Peer company data
- CompanyDividend: Dividend information
- CompanyTechnicalIndicator: Technical analysis indicators (SMA, RSI, etc.)
"""

import datetime
from datetime import date as date_type
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ========================
# STOCK PRICE SCHEMAS
# ========================


class StockPriceChangeBase(BaseModel):
    symbol: str
    one_day: Optional[float] = None
    five_day: Optional[float] = None
    one_month: Optional[float] = None
    three_month: Optional[float] = None
    six_month: Optional[float] = None
    ytd: Optional[float] = None
    one_year: Optional[float] = None
    three_year: Optional[float] = None
    five_year: Optional[float] = None
    ten_year: Optional[float] = None


class StockPriceChangeWrite(StockPriceChangeBase):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class StockPriceChangeRead(StockPriceChangeBase):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


class StockPrice(BaseModel):
    symbol: str
    date: datetime.datetime
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int
    after_hours_price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class StockPriceRead(StockPrice):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


class StockPriceWrite(StockPrice):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


# ========================
# STOCK SPLIT SCHEMAS
# ========================


class CompanyStockSplit(BaseModel):
    symbol: str
    date: date_type
    numerator: int
    denominator: int


class CompanyStockSplitWrite(CompanyStockSplit):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyStockSplitRead(CompanyStockSplit):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# STOCK PEER SCHEMAS
# ========================


class CompanyStockPeer(BaseModel):
    symbol: str
    company_name: str
    price: float
    market_cap: int


class CompanyStockPeerWrite(CompanyStockPeer):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyStockPeerRead(CompanyStockPeer):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# DIVIDEND SCHEMAS
# ========================


class CompanyDividend(BaseModel):
    symbol: str
    date: date_type
    record_date: Optional[date_type] = None
    payment_date: Optional[date_type] = None
    declaration_date: Optional[date_type] = None
    dividend: Optional[float] = None
    adj_dividend: Optional[float] = None
    dividend_yield: Optional[float] = None
    frequency: Optional[str] = None
    currency: Optional[str] = None


class CompanyDividendWrite(CompanyDividend):
    model_config = ConfigDict(from_attributes=True)


class CompanyDividendRead(CompanyDividend):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========================
# TECHNICAL INDICATOR SCHEMAS
# ========================


class CompanyTechnicalIndicator(BaseModel):
    symbol: str
    date: str
    simple_moving_average: Optional[float] = None
    exponential_moving_average: Optional[float] = None
    weighted_moving_average: Optional[float] = None
    double_exponential_moving_average: Optional[float] = None
    triple_exponential_moving_average: Optional[float] = None
    relative_strength_index: Optional[float] = None
    standard_deviation: Optional[float] = None
    williams_percent_r: Optional[float] = None
    average_directional_index: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyTechnicalIndicatorWrite(CompanyTechnicalIndicator):
    company_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyTechnicalIndicatorRead(CompanyTechnicalIndicator):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)
