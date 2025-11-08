import json
from datetime import date as date_type
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FMPStockSplit(BaseModel):
    symbol: str
    date: date_type
    numerator: int
    denominator: int

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("date", mode="before")
    @classmethod
    def convert_date_string_to_date(cls, v):
        """Convert date string (YYYY-MM-DD) to Python date object."""
        if isinstance(v, date_type):
            return v
        if isinstance(v, str):
            return date_type.fromisoformat(v)
        return v


class FMPStockPeer(BaseModel):
    symbol: str
    company_name: str = Field(..., alias="companyName")
    price: float
    market_cap: float = Field(..., alias="mktCap")

    model_config = ConfigDict(populate_by_name=True)


class FMPStockScreenResult(BaseModel):
    symbol: str = Field(..., description="Ticker symbol of the company")
    company_name: str = Field(..., alias="companyName", description="Full company name")
    market_cap: int = Field(
        ..., alias="marketCap", description="Market capitalization in USD"
    )
    sector: str = Field(..., description="Sector classification (e.g., Technology)")
    industry: str = Field(
        ..., description="Industry classification (e.g., Consumer Electronics)"
    )
    beta: float = Field(..., description="Beta value, volatility compared to market")
    price: float = Field(..., description="Current stock price")
    last_annual_dividend: float = Field(
        ..., alias="lastAnnualDividend", description="Most recent annual dividend"
    )
    volume: int = Field(..., description="Latest trading volume")
    exchange: str = Field(..., description="Full name of the exchange")
    exchange_short_name: str = Field(
        ..., alias="exchangeShortName", description="Short exchange name"
    )
    country: str = Field(..., description="Country of listing")
    is_etf: bool = Field(..., alias="isEtf", description="True if ETF")
    is_fund: bool = Field(..., alias="isFund", description="True if Fund")
    is_actively_trading: bool = Field(
        ..., alias="isActivelyTrading", description="True if stock is actively trading"
    )

    model_config = ConfigDict(populate_by_name=True)


class FMPStockRating(BaseModel):
    symbol: str
    rating: Optional[str] = None
    overall_score: Optional[int] = Field(None, alias="overallScore")
    discounted_cash_flow_score: Optional[int] = Field(
        None, alias="discountedCashFlowScore"
    )
    return_on_equity_score: Optional[int] = Field(None, alias="returnOnEquityScore")
    return_on_assets_score: Optional[int] = Field(None, alias="returnOnAssetsScore")
    debt_to_equity_score: Optional[int] = Field(None, alias="debtToEquityScore")
    price_to_earnings_score: Optional[int] = Field(None, alias="priceToEarningsScore")
    price_to_book_score: Optional[int] = Field(None, alias="priceToBookScore")

    model_config = ConfigDict(populate_by_name=True)


class FMPStockGrading(BaseModel):
    symbol: str
    date: date_type
    grading_company: Optional[str] = Field(None, alias="gradingCompany")
    previous_grade: Optional[str] = Field(None, alias="previousGrade")
    new_grade: Optional[str] = Field(None, alias="newGrade")
    action: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("date", mode="before")
    @classmethod
    def convert_date_string_to_date(cls, v):
        """Convert date string (YYYY-MM-DD) to Python date object."""
        if isinstance(v, date_type):
            return v
        if isinstance(v, str):
            return date_type.fromisoformat(v)
        return v


class FMPStockGradingSummary(BaseModel):
    symbol: str
    strong_buy: int = Field(..., alias="strongBuy")
    buy: int
    hold: int
    sell: int
    strong_sell: int = Field(..., alias="strongSell")
    consensus: str

    model_config = ConfigDict(populate_by_name=True)


class FMPStockPriceTarget(BaseModel):
    symbol: str
    target_high: Optional[float] = Field(None, alias="targetHigh")
    target_low: Optional[float] = Field(None, alias="targetLow")
    target_consensus: Optional[float] = Field(None, alias="targetConsensus")
    target_median: Optional[float] = Field(None, alias="targetMedian")

    model_config = ConfigDict(populate_by_name=True)


class FMPStockPriceTargetSummary(BaseModel):
    symbol: str
    last_month_count: Optional[int] = Field(None, alias="lastMonthCount")
    last_month_average_price_target: Optional[float] = Field(
        None, alias="lastMonthAvgPriceTarget"
    )
    last_quarter_count: Optional[int] = Field(None, alias="lastQuarterCount")
    last_quarter_average_price_target: Optional[float] = Field(
        None, alias="lastQuarterAvgPriceTarget"
    )
    last_year_count: Optional[int] = Field(None, alias="lastYearCount")
    last_year_average_price_target: Optional[float] = Field(
        None, alias="lastYearAvgPriceTarget"
    )
    all_time_count: Optional[int] = Field(None, alias="allTimeCount")
    all_time_average_price_target: Optional[float] = Field(
        None, alias="allTimeAvgPriceTarget"
    )
    publishers: Optional[List[str]] = None

    @field_validator("publishers", mode="before")
    @classmethod
    def parse_publishers(cls, v):
        """
        Parse publishers field which can come as:
        - JSON string: "[\"TheFly\",\"StreetInsider\"]"
        - List: ["TheFly", "StreetInsider"]
        - None/null
        """
        if v is None:
            return None

        # If it's already a list, return as-is
        if isinstance(v, list):
            return v

        # If it's a string, try to parse as JSON
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                # Ensure the parsed result is a list
                if isinstance(parsed, list):
                    return parsed
                else:
                    # If JSON parsing gives us something else, wrap in list
                    return [str(parsed)]
            except (json.JSONDecodeError, TypeError):
                # If JSON parsing fails, try to split by comma or return as single item
                if "," in v:
                    # Remove brackets and quotes, then split
                    cleaned = v.strip('[]"')
                    return [item.strip().strip('"') for item in cleaned.split(",")]
                else:
                    # Return as single item list
                    return [v.strip('[]"')]

        # For any other type, convert to string and wrap in list
        return [str(v)]

    model_config = ConfigDict(populate_by_name=True)
