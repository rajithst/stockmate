from pydantic import BaseModel, Field, ConfigDict


class FMPAnalystEstimates(BaseModel):
    symbol: str
    date: str

    revenue_low: int = Field(..., alias="revenueLow")
    revenue_high: int = Field(..., alias="revenueHigh")
    revenue_avg: int = Field(..., alias="revenueAvg")

    ebitda_low: int = Field(..., alias="ebitdaLow")
    ebitda_high: int = Field(..., alias="ebitdaHigh")
    ebitda_avg: int = Field(..., alias="ebitdaAvg")

    ebit_low: int = Field(..., alias="ebitLow")
    ebit_high: int = Field(..., alias="ebitHigh")
    ebit_avg: int = Field(..., alias="ebitAvg")

    net_income_low: int = Field(..., alias="netIncomeLow")
    net_income_high: int = Field(..., alias="netIncomeHigh")
    net_income_avg: int = Field(..., alias="netIncomeAvg")

    sga_expense_low: int = Field(..., alias="sgaExpenseLow")
    sga_expense_high: int = Field(..., alias="sgaExpenseHigh")
    sga_expense_avg: int = Field(..., alias="sgaExpenseAvg")

    eps_avg: float = Field(..., alias="epsAvg")
    eps_high: float = Field(..., alias="epsHigh")
    eps_low: float = Field(..., alias="epsLow")

    num_analysts_revenue: int = Field(..., alias="numAnalystsRevenue")
    num_analysts_eps: int = Field(..., alias="numAnalystsEps")

    model_config = ConfigDict(populate_by_name=True)
