from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class FMPDFCValuation(BaseModel):
    symbol: str
    date: date
    dcf: float
    stock_price: float = Field(..., alias="Stock Price")

    model_config = ConfigDict(populate_by_name=True)


class FMPCustomDFCValuation(BaseModel):
    year: str
    symbol: str
    revenue: float
    revenue_percentage: float = Field(..., alias="revenuePercentage")
    ebitda: float
    ebitda_percentage: float = Field(..., alias="ebitdaPercentage")
    ebit: float
    ebit_percentage: float = Field(..., alias="ebitPercentage")
    depreciation: float
    depreciation_percentage: float = Field(..., alias="depreciationPercentage")
    total_cash: float = Field(..., alias="totalCash")
    total_cash_percentage: float = Field(..., alias="totalCashPercentage")
    receivables: float
    receivables_percentage: float = Field(..., alias="receivablesPercentage")
    inventories: float
    inventories_percentage: float = Field(..., alias="inventoriesPercentage")
    payable: float
    payable_percentage: float = Field(..., alias="payablePercentage")
    capital_expenditure: float = Field(..., alias="capitalExpenditure")
    capital_expenditure_percentage: float = Field(
        ..., alias="capitalExpenditurePercentage"
    )
    price: float
    beta: float
    diluted_shares_outstanding: int = Field(..., alias="dilutedSharesOutstanding")
    cost_of_debt: float = Field(..., alias="costofDebt")
    tax_rate: float = Field(..., alias="taxRate")
    after_tax_cost_of_debt: float = Field(..., alias="afterTaxCostOfDebt")
    risk_free_rate: float = Field(..., alias="riskFreeRate")
    market_risk_premium: float = Field(..., alias="marketRiskPremium")
    cost_of_equity: float = Field(..., alias="costOfEquity")
    total_debt: float = Field(..., alias="totalDebt")
    total_equity: float = Field(..., alias="totalEquity")
    total_capital: float = Field(..., alias="totalCapital")
    debt_weighting: float = Field(..., alias="debtWeighting")
    equity_weighting: float = Field(..., alias="equityWeighting")
    wacc: float
    tax_rate_cash: float = Field(..., alias="taxRateCash")
    ebiat: float
    ufcf: float
    sum_pv_ufcf: float = Field(..., alias="sumPvUfcf")
    long_term_growth_rate: float = Field(..., alias="longTermGrowthRate")
    terminal_value: float = Field(..., alias="terminalValue")
    present_terminal_value: float = Field(..., alias="presentTerminalValue")
    enterprise_value: float = Field(..., alias="enterpriseValue")
    net_debt: float = Field(..., alias="netDebt")
    equity_value: float = Field(..., alias="equityValue")
    equity_value_per_share: float = Field(..., alias="equityValuePerShare")
    free_cash_flow_t1: float = Field(..., alias="freeCashFlowT1")

    model_config = ConfigDict(populate_by_name=True)
