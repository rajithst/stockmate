from datetime import date as date_type
from pydantic import BaseModel, ConfigDict, Field, field_validator


class FMPStockPriceChange(BaseModel):
    symbol: str
    one_day: float = Field(..., alias="1D")
    five_day: float = Field(..., alias="5D")
    one_month: float = Field(..., alias="1M")
    three_month: float = Field(..., alias="3M")
    six_month: float = Field(..., alias="6M")
    ytd: float = Field(..., alias="ytd")
    one_year: float = Field(..., alias="1Y")
    three_year: float = Field(..., alias="3Y")
    five_year: float = Field(..., alias="5Y")
    ten_year: float = Field(..., alias="10Y")

    model_config = ConfigDict(populate_by_name=True)


class FMPStockHistoricalPrice(BaseModel):
    symbol: str
    date: date_type
    open: float
    high: float
    low: float
    close: float
    volume: int
    change: float
    change_percent: float = Field(..., alias="changePercent")


class FMPStockPrice(BaseModel):
    symbol: str
    date: date_type = Field(..., alias="timestamp")
    open_price: float = Field(..., alias="open")
    close_price: float = Field(..., alias="price")
    high_price: float = Field(..., alias="dayHigh")
    low_price: float = Field(..., alias="dayLow")
    volume: int
    change: float
    change_percent: float = Field(..., alias="changePercentage")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("date", mode="before")
    @classmethod
    def convert_timestamp_to_date(cls, v):
        """Convert Unix timestamp or date string to date."""
        if isinstance(v, date_type):
            return v
        if isinstance(v, int) or isinstance(v, float):
            # Unix timestamp (seconds or milliseconds since epoch)
            # Convert to datetime and extract date
            from datetime import datetime as dt

            timestamp = int(v)
            # Check if it's likely in milliseconds (> year 3000 in seconds)
            if timestamp > 32503680000:
                timestamp = timestamp // 1000
            return dt.fromtimestamp(timestamp).date()
        if isinstance(v, str):
            # Parse ISO format date string (YYYY-MM-DD)
            return date_type.fromisoformat(v)
        # If it's a datetime object, extract just the date
        if hasattr(v, "date"):
            return v.date()
        return v


class FMPAfterHoursPrice(BaseModel):
    symbol: str
    after_hours_price: float = Field(..., alias="price")

    model_config = ConfigDict(populate_by_name=True)
