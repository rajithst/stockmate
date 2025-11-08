from pydantic import BaseModel, ConfigDict, Field
from datetime import date as date_type


class FMPAnalystEstimates(BaseModel):
    symbol: str
    date: date_type = Field(..., description="Date of the estimate")

    revenue_low: float = Field(..., alias="revenueLow")
    revenue_high: float = Field(..., alias="revenueHigh")
    revenue_avg: float = Field(..., alias="revenueAvg")

    ebitda_low: float = Field(..., alias="ebitdaLow")
    ebitda_high: float = Field(..., alias="ebitdaHigh")
    ebitda_avg: float = Field(..., alias="ebitdaAvg")

    ebit_low: float = Field(..., alias="ebitLow")
    ebit_high: float = Field(..., alias="ebitHigh")
    ebit_avg: float = Field(..., alias="ebitAvg")

    net_income_low: float = Field(..., alias="netIncomeLow")
    net_income_high: float = Field(..., alias="netIncomeHigh")
    net_income_avg: float = Field(..., alias="netIncomeAvg")

    sga_expense_low: float = Field(..., alias="sgaExpenseLow")
    sga_expense_high: float = Field(..., alias="sgaExpenseHigh")
    sga_expense_avg: float = Field(..., alias="sgaExpenseAvg")

    eps_avg: float = Field(..., alias="epsAvg")
    eps_high: float = Field(..., alias="epsHigh")
    eps_low: float = Field(..., alias="epsLow")

    num_analysts_revenue: int = Field(..., alias="numAnalystsRevenue")
    num_analysts_eps: int = Field(..., alias="numAnalystsEps")

    model_config = ConfigDict(populate_by_name=True)
