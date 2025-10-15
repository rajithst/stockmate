from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompanyStockSplit(BaseModel):
    company_id: int
    symbol: str
    date: str
    numerator: int
    denominator: int


class CompanyStockSplitWrite(CompanyStockSplit):
    model_config = ConfigDict(from_attributes=True)


class CompanyStockSplitRead(CompanyStockSplit):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyStockPeer(BaseModel):
    company_id: int
    symbol: str
    company_name: str
    price: float
    market_cap: int


class CompanyStockPeerWrite(CompanyStockPeer):
    model_config = ConfigDict(from_attributes=True)


class CompanyStockPeerRead(CompanyStockPeer):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
