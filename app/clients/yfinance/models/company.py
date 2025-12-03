from datetime import date as date_type, date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class YFinanceCompanyProfile(BaseModel):
    """Comprehensive company information from yfinance

    Includes company details, pricing, valuations, and financial metrics.
    Excludes: companyOfficers, executiveTeam, corporateActions
    """

    # === BASIC COMPANY INFORMATION ===
    symbol: str = Field(..., description="Ticker symbol")
    short_name: str = Field(
        default="", alias="shortName", description="Short company name"
    )
    long_name: str = Field(..., alias="longName", description="Full company name")
    quote_type: str = Field(
        default="EQUITY",
        alias="quoteType",
        description="Type of quote (EQUITY, ETF, etc.)",
    )

    # === LOCATION & CONTACT ===
    country: Optional[str] = Field(None, description="Country of headquarters")
    state: Optional[str] = Field(None, description="State/province of headquarters")
    city: Optional[str] = Field(None, description="City of headquarters")
    address1: Optional[str] = Field(
        None, alias="address1", description="Primary address"
    )
    address2: Optional[str] = Field(
        None, alias="address2", description="Secondary address"
    )
    zip: Optional[str] = Field(None, description="Postal code")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[HttpUrl] = Field(None, description="Company website URL")
    ir_website: Optional[str] = Field(
        None, alias="irWebsite", description="Investor relations website"
    )

    # === COMPANY CLASSIFICATION ===
    industry: Optional[str] = Field(None, description="Industry name")
    industry_key: Optional[str] = Field(
        None, alias="industryKey", description="Industry key"
    )
    industry_display: Optional[str] = Field(
        None, alias="industryDisp", description="Industry display name"
    )
    sector: Optional[str] = Field(None, description="Sector name")
    sector_key: Optional[str] = Field(None, alias="sectorKey", description="Sector key")
    sector_display: Optional[str] = Field(
        None, alias="sectorDisp", description="Sector display name"
    )

    # === COMPANY DESCRIPTION & DETAILS ===
    long_business_summary: Optional[str] = Field(
        None, alias="longBusinessSummary", description="Full business description"
    )
    description: Optional[str] = Field(None, description="Short description")
    full_time_employees: Optional[int] = Field(
        None, alias="fullTimeEmployees", description="Full-time employee count"
    )
    image: Optional[HttpUrl] = Field(None, description="Company logo URL")
    default_image: Optional[bool] = Field(
        None, alias="defaultImage", description="Whether using default image"
    )

    # === EXCHANGE INFORMATION ===
    exchange: str = Field(..., description="Exchange code")
    full_exchange_name: str = Field(
        ..., alias="fullExchangeName", description="Full exchange name"
    )
    market: Optional[str] = Field(None, description="Market code")
    market_state: Optional[str] = Field(
        None,
        alias="marketState",
        description="Current market state (OPEN, CLOSED, etc.)",
    )

    # === IPO & TRADING INFO ===
    ipo_date: Optional[date_type] = Field(None, alias="ipoDate", description="IPO date")

    # === PRICING INFORMATION ===
    currency: str = Field(..., description="Currency code")
    current_price: Optional[float] = Field(
        None, alias="currentPrice", description="Current price"
    )
    previous_close: Optional[float] = Field(
        None, alias="previousClose", description="Previous close price"
    )
    open: Optional[float] = Field(None, description="Today's open price")
    day_low: Optional[float] = Field(
        None, alias="dayLow", description="Today's low price"
    )
    day_high: Optional[float] = Field(
        None, alias="dayHigh", description="Today's high price"
    )
    regular_market_previous_close: Optional[float] = Field(
        None,
        alias="regularMarketPreviousClose",
        description="Regular market previous close",
    )
    regular_market_open: Optional[float] = Field(
        None, alias="regularMarketOpen", description="Regular market open"
    )
    regular_market_day_low: Optional[float] = Field(
        None, alias="regularMarketDayLow", description="Regular market day low"
    )
    regular_market_day_high: Optional[float] = Field(
        None, alias="regularMarketDayHigh", description="Regular market day high"
    )
    regular_market_price: Optional[float] = Field(
        None, alias="regularMarketPrice", description="Regular market price"
    )
    regular_market_change: Optional[float] = Field(
        None, alias="regularMarketChange", description="Regular market change"
    )
    regular_market_change_percent: Optional[float] = Field(
        None, alias="regularMarketChangePercent", description="Regular market change %"
    )
    bid: Optional[float] = Field(None, description="Bid price")
    ask: Optional[float] = Field(None, description="Ask price")
    bid_size: Optional[int] = Field(None, alias="bidSize", description="Bid size")
    ask_size: Optional[int] = Field(None, alias="askSize", description="Ask size")
    price_hint: Optional[int] = Field(None, alias="priceHint", description="Price hint")

    # === VOLUME INFORMATION ===
    volume: Optional[int] = Field(None, description="Current day volume")
    regular_market_volume: Optional[int] = Field(
        None, alias="regularMarketVolume", description="Regular market volume"
    )
    average_volume: Optional[int] = Field(
        None, alias="averageVolume", description="Average volume"
    )
    average_volume_10_days: Optional[int] = Field(
        None, alias="averageVolume10days", description="10-day average volume"
    )
    average_daily_volume_10_day: Optional[int] = Field(
        None, alias="averageDailyVolume10Day", description="10-day average daily volume"
    )
    average_daily_volume_3_month: Optional[int] = Field(
        None,
        alias="averageDailyVolume3Month",
        description="3-month average daily volume",
    )

    # === MARKET CAPITALIZATION & SHARES ===
    market_cap: Optional[float] = Field(
        None, alias="marketCap", description="Market capitalization"
    )
    enterprise_value: Optional[float] = Field(
        None, alias="enterpriseValue", description="Enterprise value"
    )
    shares_outstanding: Optional[int] = Field(
        None, alias="sharesOutstanding", description="Outstanding shares"
    )
    implied_shares_outstanding: Optional[int] = Field(
        None, alias="impliedSharesOutstanding", description="Implied outstanding shares"
    )
    float_shares: Optional[int] = Field(
        None, alias="floatShares", description="Float shares"
    )
    held_percent_insiders: Optional[float] = Field(
        None, alias="heldPercentInsiders", description="Insider ownership %"
    )
    held_percent_institutions: Optional[float] = Field(
        None, alias="heldPercentInstitutions", description="Institutional ownership %"
    )

    # === 52 WEEK INFORMATION ===
    fifty_two_week_low: Optional[float] = Field(
        None, alias="fiftyTwoWeekLow", description="52-week low"
    )
    fifty_two_week_high: Optional[float] = Field(
        None, alias="fiftyTwoWeekHigh", description="52-week high"
    )
    fifty_two_week_low_change: Optional[float] = Field(
        None, alias="fiftyTwoWeekLowChange", description="Change from 52-week low"
    )
    fifty_two_week_low_change_percent: Optional[float] = Field(
        None,
        alias="fiftyTwoWeekLowChangePercent",
        description="Change from 52-week low %",
    )
    fifty_two_week_high_change: Optional[float] = Field(
        None, alias="fiftyTwoWeekHighChange", description="Change from 52-week high"
    )
    fifty_two_week_high_change_percent: Optional[float] = Field(
        None,
        alias="fiftyTwoWeekHighChangePercent",
        description="Change from 52-week high %",
    )
    fifty_two_week_range: Optional[str] = Field(
        None, alias="fiftyTwoWeekRange", description="52-week range"
    )
    fifty_two_week_change: Optional[float] = Field(
        None, alias="52WeekChange", description="52-week change"
    )
    fifty_two_week_change_percent: Optional[float] = Field(
        None, alias="fiftyTwoWeekChangePercent", description="52-week change %"
    )

    # === ALL TIME HIGH/LOW ===
    all_time_high: Optional[float] = Field(
        None, alias="allTimeHigh", description="All-time high price"
    )
    all_time_low: Optional[float] = Field(
        None, alias="allTimeLow", description="All-time low price"
    )

    # === MOVING AVERAGES ===
    fifty_day_average: Optional[float] = Field(
        None, alias="fiftyDayAverage", description="50-day average"
    )
    fifty_day_average_change: Optional[float] = Field(
        None, alias="fiftyDayAverageChange", description="50-day average change"
    )
    fifty_day_average_change_percent: Optional[float] = Field(
        None,
        alias="fiftyDayAverageChangePercent",
        description="50-day average change %",
    )
    two_hundred_day_average: Optional[float] = Field(
        None, alias="twoHundredDayAverage", description="200-day average"
    )
    two_hundred_day_average_change: Optional[float] = Field(
        None, alias="twoHundredDayAverageChange", description="200-day average change"
    )
    two_hundred_day_average_change_percent: Optional[float] = Field(
        None,
        alias="twoHundredDayAverageChangePercent",
        description="200-day average change %",
    )

    # === DIVIDEND INFORMATION ===
    dividend_rate: Optional[float] = Field(
        None, alias="dividendRate", description="Annual dividend rate"
    )
    dividend_yield: Optional[float] = Field(
        None, alias="dividendYield", description="Dividend yield"
    )
    trailing_annual_dividend_rate: Optional[float] = Field(
        None,
        alias="trailingAnnualDividendRate",
        description="Trailing annual dividend rate",
    )
    trailing_annual_dividend_yield: Optional[float] = Field(
        None,
        alias="trailingAnnualDividendYield",
        description="Trailing annual dividend yield",
    )
    five_year_avg_dividend_yield: Optional[float] = Field(
        None,
        alias="fiveYearAvgDividendYield",
        description="5-year average dividend yield",
    )
    ex_dividend_date: Optional[int] = Field(
        None, alias="exDividendDate", description="Ex-dividend date (epoch)"
    )
    last_dividend_date: Optional[int] = Field(
        None, alias="lastDividendDate", description="Last dividend date (epoch)"
    )
    last_dividend_value: Optional[float] = Field(
        None, alias="lastDividendValue", description="Last dividend value"
    )
    payout_ratio: Optional[float] = Field(
        None, alias="payoutRatio", description="Payout ratio"
    )

    # === VALUATION RATIOS ===
    trailing_pe: Optional[float] = Field(
        None, alias="trailingPE", description="Trailing P/E ratio"
    )
    forward_pe: Optional[float] = Field(
        None, alias="forwardPE", description="Forward P/E ratio"
    )
    trailing_peg_ratio: Optional[float] = Field(
        None, alias="trailingPegRatio", description="Trailing PEG ratio"
    )
    price_to_sales_trailing_12_months: Optional[float] = Field(
        None,
        alias="priceToSalesTrailing12Months",
        description="P/S ratio (trailing 12 months)",
    )
    price_to_book: Optional[float] = Field(
        None, alias="priceToBook", description="P/B ratio"
    )
    enterprise_to_revenue: Optional[float] = Field(
        None, alias="enterpriseToRevenue", description="EV/Revenue ratio"
    )

    # === EARNINGS & EPS ===
    trailing_eps: Optional[float] = Field(
        None, alias="trailingEps", description="Trailing EPS"
    )
    forward_eps: Optional[float] = Field(
        None, alias="forwardEps", description="Forward EPS"
    )
    eps_trailing_twelve_months: Optional[float] = Field(
        None, alias="epsTrailingTwelveMonths", description="EPS (trailing 12 months)"
    )
    eps_for_forward: Optional[float] = Field(
        None, alias="epsForward", description="EPS forward"
    )
    earnings_growth: Optional[float] = Field(
        None, alias="earningsGrowth", description="Earnings growth rate"
    )
    earnings_quarterly_growth: Optional[float] = Field(
        None, alias="earningsQuarterlyGrowth", description="Quarterly earnings growth"
    )
    net_income_to_common: Optional[float] = Field(
        None, alias="netIncomeToCommon", description="Net income to common"
    )

    # === FINANCIAL METRICS ===
    book_value: Optional[float] = Field(
        None, alias="bookValue", description="Book value per share"
    )
    total_cash: Optional[float] = Field(
        None, alias="totalCash", description="Total cash"
    )
    total_cash_per_share: Optional[float] = Field(
        None, alias="totalCashPerShare", description="Cash per share"
    )
    total_debt: Optional[float] = Field(
        None, alias="totalDebt", description="Total debt"
    )
    total_revenue: Optional[float] = Field(
        None, alias="totalRevenue", description="Total revenue"
    )
    revenue_per_share: Optional[float] = Field(
        None, alias="revenuePerShare", description="Revenue per share"
    )
    gross_profits: Optional[float] = Field(
        None, alias="grossProfits", description="Gross profits"
    )
    beta: Optional[float] = Field(None, description="Beta coefficient")

    # === PROFITABILITY & MARGINS ===
    profit_margins: Optional[float] = Field(
        None, alias="profitMargins", description="Profit margin"
    )
    gross_margins: Optional[float] = Field(
        None, alias="grossMargins", description="Gross margin"
    )
    operating_margins: Optional[float] = Field(
        None, alias="operatingMargins", description="Operating margin"
    )
    ebitda_margins: Optional[float] = Field(
        None, alias="ebitdaMargins", description="EBITDA margin"
    )

    # === RETURNS ===
    return_on_assets: Optional[float] = Field(
        None, alias="returnOnAssets", description="Return on assets"
    )
    return_on_equity: Optional[float] = Field(
        None, alias="returnOnEquity", description="Return on equity"
    )

    # === GROWTH ===
    revenue_growth: Optional[float] = Field(
        None, alias="revenueGrowth", description="Revenue growth rate"
    )

    # === ANALYST INFORMATION ===
    number_of_analyst_opinions: Optional[int] = Field(
        None, alias="numberOfAnalystOpinions", description="Number of analyst opinions"
    )
    recommendation_key: Optional[str] = Field(
        None,
        alias="recommendationKey",
        description="Recommendation (buy, hold, sell, etc.)",
    )
    recommendation_mean: Optional[float] = Field(
        None, alias="recommendationMean", description="Mean recommendation score"
    )
    average_analyst_rating: Optional[str] = Field(
        None, alias="averageAnalystRating", description="Average analyst rating"
    )
    target_mean_price: Optional[float] = Field(
        None, alias="targetMeanPrice", description="Mean target price"
    )
    target_median_price: Optional[float] = Field(
        None, alias="targetMedianPrice", description="Median target price"
    )
    target_high_price: Optional[float] = Field(
        None, alias="targetHighPrice", description="High target price"
    )
    target_low_price: Optional[float] = Field(
        None, alias="targetLowPrice", description="Low target price"
    )

    # === FISCAL YEAR INFORMATION ===
    last_fiscal_year_end: Optional[int] = Field(
        None, alias="lastFiscalYearEnd", description="Last fiscal year end (epoch)"
    )
    next_fiscal_year_end: Optional[int] = Field(
        None, alias="nextFiscalYearEnd", description="Next fiscal year end (epoch)"
    )
    most_recent_quarter: Optional[int] = Field(
        None, alias="mostRecentQuarter", description="Most recent quarter (epoch)"
    )

    # === EARNINGS CALL INFORMATION ===
    earnings_timestamp: Optional[int] = Field(
        None, alias="earningsTimestamp", description="Earnings timestamp (epoch)"
    )
    earnings_timestamp_start: Optional[int] = Field(
        None,
        alias="earningsTimestampStart",
        description="Earnings period start (epoch)",
    )
    earnings_timestamp_end: Optional[int] = Field(
        None, alias="earningsTimestampEnd", description="Earnings period end (epoch)"
    )
    earnings_call_timestamp_start: Optional[int] = Field(
        None,
        alias="earningsCallTimestampStart",
        description="Earnings call start (epoch)",
    )
    earnings_call_timestamp_end: Optional[int] = Field(
        None, alias="earningsCallTimestampEnd", description="Earnings call end (epoch)"
    )
    is_earnings_date_estimate: Optional[bool] = Field(
        None,
        alias="isEarningsDateEstimate",
        description="Whether earnings date is estimated",
    )

    # === STOCK SPLIT INFORMATION ===
    last_split_factor: Optional[str] = Field(
        None, alias="lastSplitFactor", description="Last stock split factor"
    )
    last_split_date: Optional[int] = Field(
        None, alias="lastSplitDate", description="Last stock split date (epoch)"
    )

    # === GOVERNANCE & RISK ===
    audit_risk: Optional[int] = Field(
        None, alias="auditRisk", description="Audit risk score"
    )
    board_risk: Optional[int] = Field(
        None, alias="boardRisk", description="Board risk score"
    )
    compensation_risk: Optional[int] = Field(
        None, alias="compensationRisk", description="Compensation risk score"
    )
    share_holder_rights_risk: Optional[int] = Field(
        None, alias="shareHolderRightsRisk", description="Shareholder rights risk score"
    )
    overall_risk: Optional[int] = Field(
        None, alias="overallRisk", description="Overall governance risk score"
    )
    governance_epoch_date: Optional[int] = Field(
        None, alias="governanceEpochDate", description="Governance data date (epoch)"
    )
    compensation_as_of_epoch_date: Optional[int] = Field(
        None,
        alias="compensationAsOfEpochDate",
        description="Compensation data date (epoch)",
    )

    # === MISCELLANEOUS ===
    quote_source_name: Optional[str] = Field(
        None, alias="quoteSourceName", description="Quote source"
    )
    triggerable: Optional[bool] = Field(None, description="Whether triggerable")
    custom_price_alert_confidence: Optional[str] = Field(
        None, alias="customPriceAlertConfidence", description="Price alert confidence"
    )
    source_interval: Optional[int] = Field(
        None, alias="sourceInterval", description="Source interval"
    )
    exchange_data_delayed_by: Optional[int] = Field(
        None, alias="exchangeDataDelayedBy", description="Data delay in seconds"
    )
    message_board_id: Optional[str] = Field(
        None, alias="messageBoardId", description="Message board ID"
    )
    has_pre_post_market_data: Optional[bool] = Field(
        None, alias="hasPrePostMarketData", description="Has pre/post market data"
    )
    esg_populated: Optional[bool] = Field(
        None, alias="esgPopulated", description="ESG data populated"
    )
    region: Optional[str] = Field(None, description="Region code")
    language: Optional[str] = Field(None, description="Language code")
    type_display: Optional[str] = Field(
        None, alias="typeDisp", description="Type display name"
    )
    regular_market_day_range: Optional[str] = Field(
        None, alias="regularMarketDayRange", description="Regular market day range"
    )
    regular_market_time: Optional[int] = Field(
        None, alias="regularMarketTime", description="Regular market time (epoch)"
    )
    sand_p_52_week_change: Optional[float] = Field(
        None, alias="SandP52WeekChange", description="S&P 500 52-week change"
    )
    max_age: Optional[int] = Field(None, alias="maxAge", description="Max age of data")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("ipo_date", mode="before")
    @classmethod
    def convert_ipo_date(cls, v):
        """Convert IPO date string to date object if needed."""
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v


class YFinanceDividend(BaseModel):
    symbol: str
    date: date_type
    record_date: Optional[float] = None
    payment_date: date_type = Field(..., alias="date")
    declaration_date: Optional[float] = None
    adj_dividend: Optional[float] = None
    dividend: float
    dividend_yield: Optional[float] = None
    frequency: Optional[str] = None
    currency: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class YFinanceStockSplit(BaseModel):
    symbol: str
    date: date_type
    split_ratio: float = Field(..., alias="splitRatio")

    model_config = ConfigDict(populate_by_name=True)
