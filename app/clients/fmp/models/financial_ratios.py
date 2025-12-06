from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date as date_type


class FMPKeyMetrics(BaseModel):
    symbol: str
    date: date_type
    fiscal_year: str = Field(alias="fiscalYear")
    period: str
    reported_currency: str = Field(alias="reportedCurrency")

    market_cap: float = Field(alias="marketCap")
    enterprise_value: float = Field(alias="enterpriseValue")

    ev_to_sales: float = Field(alias="evToSales")
    ev_to_operating_cash_flow: float = Field(alias="evToOperatingCashFlow")
    ev_to_free_cash_flow: float = Field(alias="evToFreeCashFlow")
    ev_to_ebitda: float = Field(alias="evToEBITDA")

    net_debt_to_ebitda: float = Field(alias="netDebtToEBITDA")
    current_ratio: float = Field(alias="currentRatio")
    income_quality: float = Field(alias="incomeQuality")
    graham_number: float = Field(alias="grahamNumber")
    graham_net_net: float = Field(alias="grahamNetNet")
    tax_burden: float = Field(alias="taxBurden")
    interest_burden: float = Field(alias="interestBurden")

    working_capital: float = Field(alias="workingCapital")
    invested_capital: float = Field(alias="investedCapital")

    return_on_assets: float = Field(alias="returnOnAssets")
    operating_return_on_assets: float = Field(alias="operatingReturnOnAssets")
    return_on_tangible_assets: float = Field(alias="returnOnTangibleAssets")
    return_on_equity: float = Field(alias="returnOnEquity")
    return_on_invested_capital: float = Field(alias="returnOnInvestedCapital")
    return_on_capital_employed: float = Field(alias="returnOnCapitalEmployed")

    earnings_yield: float = Field(alias="earningsYield")
    free_cash_flow_yield: float = Field(alias="freeCashFlowYield")

    capex_to_operating_cash_flow: float = Field(alias="capexToOperatingCashFlow")
    capex_to_depreciation: float = Field(alias="capexToDepreciation")
    capex_to_revenue: float = Field(alias="capexToRevenue")

    sales_general_and_administrative_to_revenue: float = Field(
        alias="salesGeneralAndAdministrativeToRevenue"
    )
    research_and_development_to_revenue: float = Field(
        alias="researchAndDevelopementToRevenue"
    )
    stock_based_compensation_to_revenue: float = Field(
        alias="stockBasedCompensationToRevenue"
    )
    intangibles_to_total_assets: float = Field(alias="intangiblesToTotalAssets")

    average_receivables: float = Field(alias="averageReceivables")
    average_payables: float = Field(alias="averagePayables")
    average_inventory: float = Field(alias="averageInventory")

    days_of_sales_outstanding: float = Field(alias="daysOfSalesOutstanding")
    days_of_payables_outstanding: float = Field(alias="daysOfPayablesOutstanding")
    days_of_inventory_outstanding: float = Field(alias="daysOfInventoryOutstanding")

    operating_cycle: float = Field(alias="operatingCycle")
    cash_conversion_cycle: float = Field(alias="cashConversionCycle")

    free_cash_flow_to_equity: float = Field(alias="freeCashFlowToEquity")
    free_cash_flow_to_firm: float = Field(alias="freeCashFlowToFirm")

    tangible_asset_value: float = Field(alias="tangibleAssetValue")
    net_current_asset_value: float = Field(alias="netCurrentAssetValue")

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


class FMPKeyMetricsTTM(BaseModel):
    symbol: str

    market_cap: float = Field(alias="marketCap")
    enterprise_value: float = Field(alias="enterpriseValueTTM")

    ev_to_sales: float = Field(alias="evToSalesTTM")
    ev_to_operating_cash_flow: float = Field(alias="evToOperatingCashFlowTTM")
    ev_to_free_cash_flow: float = Field(alias="evToFreeCashFlowTTM")
    ev_to_ebitda: float = Field(alias="evToEBITDATTM")

    net_debt_to_ebitda: float = Field(alias="netDebtToEBITDATTM")
    current_ratio: float = Field(alias="currentRatioTTM")
    income_quality: float = Field(alias="incomeQualityTTM")
    graham_number: float = Field(alias="grahamNumberTTM")
    graham_net_net: float = Field(alias="grahamNetNetTTM")
    tax_burden: float = Field(alias="taxBurdenTTM")
    interest_burden: float = Field(alias="interestBurdenTTM")

    working_capital: float = Field(alias="workingCapitalTTM")
    invested_capital: float = Field(alias="investedCapitalTTM")

    return_on_assets: float = Field(alias="returnOnAssetsTTM")
    operating_return_on_assets: float = Field(alias="operatingReturnOnAssetsTTM")
    return_on_tangible_assets: float = Field(alias="returnOnTangibleAssetsTTM")
    return_on_equity: float = Field(alias="returnOnEquityTTM")
    return_on_invested_capital: float = Field(alias="returnOnInvestedCapitalTTM")
    return_on_capital_employed: float = Field(alias="returnOnCapitalEmployedTTM")

    earnings_yield: float = Field(alias="earningsYieldTTM")
    free_cash_flow_yield: float = Field(alias="freeCashFlowYieldTTM")

    capex_to_operating_cash_flow: float = Field(alias="capexToOperatingCashFlowTTM")
    capex_to_depreciation: float = Field(alias="capexToDepreciationTTM")
    capex_to_revenue: float = Field(alias="capexToRevenueTTM")

    sales_general_and_administrative_to_revenue: float = Field(
        alias="salesGeneralAndAdministrativeToRevenueTTM"
    )
    research_and_development_to_revenue: float = Field(
        alias="researchAndDevelopementToRevenueTTM"
    )
    stock_based_compensation_to_revenue: float = Field(
        alias="stockBasedCompensationToRevenueTTM"
    )
    intangibles_to_total_assets: float = Field(alias="intangiblesToTotalAssetsTTM")

    average_receivables: float = Field(alias="averageReceivablesTTM")
    average_payables: float = Field(alias="averagePayablesTTM")
    average_inventory: float = Field(alias="averageInventoryTTM")

    days_of_sales_outstanding: float = Field(alias="daysOfSalesOutstandingTTM")
    days_of_payables_outstanding: float = Field(alias="daysOfPayablesOutstandingTTM")
    days_of_inventory_outstanding: float = Field(alias="daysOfInventoryOutstandingTTM")

    operating_cycle: float = Field(alias="operatingCycleTTM")
    cash_conversion_cycle: float = Field(alias="cashConversionCycleTTM")
    free_cash_flow_to_equity: float = Field(alias="freeCashFlowToEquityTTM")
    free_cash_flow_to_firm: float = Field(alias="freeCashFlowToFirmTTM")

    tangible_asset_value: float = Field(alias="tangibleAssetValueTTM")
    net_current_asset_value: float = Field(alias="netCurrentAssetValueTTM")

    model_config = ConfigDict(populate_by_name=True)


class FMPFinancialRatios(BaseModel):
    symbol: str
    date: date_type
    fiscal_year: str = Field(None, alias="fiscalYear")
    period: str = None
    reported_currency: str = Field(None, alias="reportedCurrency")

    gross_profit_margin: Optional[float] = Field(None, alias="grossProfitMargin")
    ebit_margin: Optional[float] = Field(None, alias="ebitMargin")
    ebitda_margin: Optional[float] = Field(None, alias="ebitdaMargin")
    operating_profit_margin: Optional[float] = Field(
        None, alias="operatingProfitMargin"
    )
    pretax_profit_margin: Optional[float] = Field(None, alias="pretaxProfitMargin")
    continuous_operations_profit_margin: Optional[float] = Field(
        None, alias="continuousOperationsProfitMargin"
    )
    net_profit_margin: Optional[float] = Field(None, alias="netProfitMargin")
    bottom_line_profit_margin: Optional[float] = Field(
        None, alias="bottomLineProfitMargin"
    )

    receivables_turnover: Optional[float] = Field(None, alias="receivablesTurnover")
    payables_turnover: Optional[float] = Field(None, alias="payablesTurnover")
    inventory_turnover: Optional[float] = Field(None, alias="inventoryTurnover")
    fixed_asset_turnover: Optional[float] = Field(None, alias="fixedAssetTurnover")
    asset_turnover: Optional[float] = Field(None, alias="assetTurnover")

    current_ratio: Optional[float] = Field(None, alias="currentRatio")
    quick_ratio: Optional[float] = Field(None, alias="quickRatio")
    solvency_ratio: Optional[float] = Field(None, alias="solvencyRatio")
    cash_ratio: Optional[float] = Field(None, alias="cashRatio")

    price_to_earnings_ratio: Optional[float] = Field(None, alias="priceToEarningsRatio")
    price_to_earnings_growth_ratio: Optional[float] = Field(
        None, alias="priceToEarningsGrowthRatio"
    )
    forward_price_to_earnings_growth_ratio: Optional[float] = Field(
        None, alias="forwardPriceToEarningsGrowthRatio"
    )
    price_to_book_ratio: Optional[float] = Field(None, alias="priceToBookRatio")
    price_to_sales_ratio: Optional[float] = Field(None, alias="priceToSalesRatio")
    price_to_free_cash_flow_ratio: Optional[float] = Field(
        None, alias="priceToFreeCashFlowRatio"
    )
    price_to_operating_cash_flow_ratio: Optional[float] = Field(
        None, alias="priceToOperatingCashFlowRatio"
    )

    debt_to_assets_ratio: Optional[float] = Field(None, alias="debtToAssetsRatio")
    debt_to_equity_ratio: Optional[float] = Field(None, alias="debtToEquityRatio")
    debt_to_capital_ratio: Optional[float] = Field(None, alias="debtToCapitalRatio")
    long_term_debt_to_capital_ratio: Optional[float] = Field(
        None, alias="longTermDebtToCapitalRatio"
    )
    financial_leverage_ratio: Optional[float] = Field(
        None, alias="financialLeverageRatio"
    )

    working_capital_turnover_ratio: Optional[float] = Field(
        None, alias="workingCapitalTurnoverRatio"
    )
    operating_cash_flow_ratio: Optional[float] = Field(
        None, alias="operatingCashFlowRatio"
    )
    operating_cash_flow_sales_ratio: Optional[float] = Field(
        None, alias="operatingCashFlowSalesRatio"
    )
    free_cash_flow_operating_cash_flow_ratio: Optional[float] = Field(
        None, alias="freeCashFlowOperatingCashFlowRatio"
    )
    debt_service_coverage_ratio: Optional[float] = Field(
        None, alias="debtServiceCoverageRatio"
    )
    interest_coverage_ratio: Optional[float] = Field(
        None, alias="interestCoverageRatio"
    )
    short_term_operating_cash_flow_coverage_ratio: Optional[float] = Field(
        None, alias="shortTermOperatingCashFlowCoverageRatio"
    )
    operating_cash_flow_coverage_ratio: Optional[float] = Field(
        None, alias="operatingCashFlowCoverageRatio"
    )
    capital_expenditure_coverage_ratio: Optional[float] = Field(
        None, alias="capitalExpenditureCoverageRatio"
    )
    dividend_paid_and_capex_coverage_ratio: Optional[float] = Field(
        None, alias="dividendPaidAndCapexCoverageRatio"
    )

    dividend_payout_ratio: Optional[float] = Field(None, alias="dividendPayoutRatio")
    dividend_yield: Optional[float] = Field(None, alias="dividendYield")
    dividend_yield_percentage: Optional[float] = Field(
        None, alias="dividendYieldPercentage"
    )

    revenue_per_share: Optional[float] = Field(None, alias="revenuePerShare")
    net_income_per_share: Optional[float] = Field(None, alias="netIncomePerShare")
    interest_debt_per_share: Optional[float] = Field(None, alias="interestDebtPerShare")
    cash_per_share: Optional[float] = Field(None, alias="cashPerShare")
    book_value_per_share: Optional[float] = Field(None, alias="bookValuePerShare")
    tangible_book_value_per_share: Optional[float] = Field(
        None, alias="tangibleBookValuePerShare"
    )
    shareholders_equity_per_share: Optional[float] = Field(
        None, alias="shareholdersEquityPerShare"
    )
    operating_cash_flow_per_share: Optional[float] = Field(
        None, alias="operatingCashFlowPerShare"
    )
    capex_per_share: Optional[float] = Field(None, alias="capexPerShare")
    free_cash_flow_per_share: Optional[float] = Field(
        None, alias="freeCashFlowPerShare"
    )

    net_income_per_ebt: Optional[float] = Field(None, alias="netIncomePerEBT")
    ebt_per_ebit: Optional[float] = Field(None, alias="ebtPerEbit")
    price_to_fair_value: Optional[float] = Field(None, alias="priceToFairValue")
    debt_to_market_cap: Optional[float] = Field(None, alias="debtToMarketCap")
    effective_tax_rate: Optional[float] = Field(None, alias="effectiveTaxRate")
    enterprise_value_multiple: Optional[float] = Field(
        None, alias="enterpriseValueMultiple"
    )

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


class FMPFinancialRatiosTTM(BaseModel):
    symbol: str
    gross_profit_margin: Optional[float] = Field(None, alias="grossProfitMarginTTM")
    ebit_margin: Optional[float] = Field(None, alias="ebitMarginTTM")
    ebitda_margin: Optional[float] = Field(None, alias="ebitdaMarginTTM")
    operating_profit_margin: Optional[float] = Field(
        None, alias="operatingProfitMarginTTM"
    )
    pretax_profit_margin: Optional[float] = Field(None, alias="pretaxProfitMarginTTM")
    continuous_operations_profit_margin: Optional[float] = Field(
        None, alias="continuousOperationsProfitMarginTTM"
    )
    net_profit_margin: Optional[float] = Field(None, alias="netProfitMarginTTM")
    bottom_line_profit_margin: Optional[float] = Field(
        None, alias="bottomLineProfitMarginTTM"
    )

    receivables_turnover: Optional[float] = Field(None, alias="receivablesTurnoverTTM")
    payables_turnover: Optional[float] = Field(None, alias="payablesTurnoverTTM")
    inventory_turnover: Optional[float] = Field(None, alias="inventoryTurnoverTTM")
    fixed_asset_turnover: Optional[float] = Field(None, alias="fixedAssetTurnoverTTM")
    asset_turnover: Optional[float] = Field(None, alias="assetTurnoverTTM")
    current_ratio: Optional[float] = Field(None, alias="currentRatioTTM")
    quick_ratio: Optional[float] = Field(None, alias="quickRatioTTM")
    solvency_ratio: Optional[float] = Field(None, alias="solvencyRatioTTM")
    cash_ratio: Optional[float] = Field(None, alias="cashRatioTTM")
    price_to_earnings_ratio: Optional[float] = Field(
        None, alias="priceToEarningsRatioTTM"
    )
    price_to_earnings_growth_ratio: Optional[float] = Field(
        None, alias="priceToEarningsGrowthRatioTTM"
    )
    forward_price_to_earnings_growth_ratio: Optional[float] = Field(
        None, alias="forwardPriceToEarningsGrowthRatioTTM"
    )
    price_to_book_ratio: Optional[float] = Field(None, alias="priceToBookRatioTTM")
    price_to_sales_ratio: Optional[float] = Field(None, alias="priceToSalesRatioTTM")
    price_to_free_cash_flow_ratio: Optional[float] = Field(
        None, alias="priceToFreeCashFlowRatioTTM"
    )
    price_to_operating_cash_flow_ratio: Optional[float] = Field(
        None, alias="priceToOperatingCashFlowRatioTTM"
    )

    debt_to_assets_ratio: Optional[float] = Field(None, alias="debtToAssetsRatioTTM")
    debt_to_equity_ratio: Optional[float] = Field(None, alias="debtToEquityRatioTTM")
    debt_to_capital_ratio: Optional[float] = Field(None, alias="debtToCapitalRatioTTM")
    long_term_debt_to_capital_ratio: Optional[float] = Field(
        None, alias="longTermDebtToCapitalRatioTTM"
    )
    financial_leverage_ratio: Optional[float] = Field(
        None, alias="financialLeverageRatioTTM"
    )

    working_capital_turnover_ratio: Optional[float] = Field(
        None, alias="workingCapitalTurnoverRatioTTM"
    )
    operating_cash_flow_ratio: Optional[float] = Field(
        None, alias="operatingCashFlowRatioTTM"
    )
    operating_cash_flow_sales_ratio: Optional[float] = Field(
        None, alias="operatingCashFlowSalesRatioTTM"
    )
    free_cash_flow_operating_cash_flow_ratio: Optional[float] = Field(
        None, alias="freeCashFlowOperatingCashFlowRatioTTM"
    )
    debt_service_coverage_ratio: Optional[float] = Field(
        None, alias="debtServiceCoverageRatioTTM"
    )
    interest_coverage_ratio: Optional[float] = Field(
        None, alias="interestCoverageRatioTTM"
    )
    short_term_operating_cash_flow_coverage_ratio: Optional[float] = Field(
        None, alias="shortTermOperatingCashFlowCoverageRatioTTM"
    )
    operating_cash_flow_coverage_ratio: Optional[float] = Field(
        None, alias="operatingCashFlowCoverageRatioTTM"
    )
    capital_expenditure_coverage_ratio: Optional[float] = Field(
        None, alias="capitalExpenditureCoverageRatioTTM"
    )
    dividend_paid_and_capex_coverage_ratio: Optional[float] = Field(
        None, alias="dividendPaidAndCapexCoverageRatioTTM"
    )

    dividend_payout_ratio: Optional[float] = Field(None, alias="dividendPayoutRatioTTM")
    dividend_yield: Optional[float] = Field(None, alias="dividendYieldTTM")
    dividend_yield_percentage: Optional[float] = Field(
        None, alias="dividendYieldPercentageTTM"
    )

    revenue_per_share: Optional[float] = Field(None, alias="revenuePerShareTTM")
    net_income_per_share: Optional[float] = Field(None, alias="netIncomePerShareTTM")
    interest_debt_per_share: Optional[float] = Field(
        None, alias="interestDebtPerShareTTM"
    )
    cash_per_share: Optional[float] = Field(None, alias="cashPerShareTTM")
    book_value_per_share: Optional[float] = Field(None, alias="bookValuePerShareTTM")
    tangible_book_value_per_share: Optional[float] = Field(
        None, alias="tangibleBookValuePerShareTTM"
    )
    shareholders_equity_per_share: Optional[float] = Field(
        None, alias="shareholdersEquityPerShareTTM"
    )
    operating_cash_flow_per_share: Optional[float] = Field(
        None, alias="operatingCashFlowPerShareTTM"
    )
    capex_per_share: Optional[float] = Field(None, alias="capexPerShareTTM")
    free_cash_flow_per_share: Optional[float] = Field(
        None, alias="freeCashFlowPerShareTTM"
    )

    net_income_per_ebt: Optional[float] = Field(None, alias="netIncomePerEBTTM")
    ebt_per_ebit: Optional[float] = Field(None, alias="ebtPerEbitTTM")
    price_to_fair_value: Optional[float] = Field(None, alias="priceToFairValueTTM")
    debt_to_market_cap: Optional[float] = Field(None, alias="debtToMarketCapTTM")
    effective_tax_rate: Optional[float] = Field(None, alias="effectiveTaxRateTTM")
    enterprise_value_multiple: Optional[float] = Field(
        None, alias="enterpriseValueMultipleTTM"
    )

    model_config = ConfigDict(populate_by_name=True)


class FMPFinancialScores(BaseModel):
    symbol: str
    reported_currency: Optional[str] = Field(None, alias="reportedCurrency")
    altman_z_score: Optional[float] = Field(None, alias="altmanZScore")
    piotroski_score: Optional[int] = Field(None, alias="piotroskiScore")
    working_capital: Optional[float] = Field(None, alias="workingCapital")
    total_assets: Optional[float] = Field(None, alias="totalAssets")
    retained_earnings: Optional[float] = Field(None, alias="retainedEarnings")
    ebit: Optional[float] = None
    market_cap: Optional[float] = Field(None, alias="marketCap")
    total_liabilities: Optional[float] = Field(None, alias="totalLiabilities")
    revenue: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)
