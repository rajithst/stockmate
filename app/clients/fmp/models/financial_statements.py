from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date as date_type


class FMPCompanyIncomeStatement(BaseModel):
    date: date_type = Field(..., description="Financial report date")
    symbol: str = Field(..., description="Ticker symbol of the company")
    reported_currency: str = Field(
        ..., alias="reportedCurrency", description="Currency used in the report"
    )
    cik: str = Field(..., description="Central Index Key identifier for SEC filings")
    filing_date: str = Field(
        ..., alias="filingDate", description="Filing date of the report"
    )
    accepted_date: str = Field(
        ..., alias="acceptedDate", description="Accepted date/time by the SEC"
    )
    fiscal_year: str = Field(
        ..., alias="fiscalYear", description="Fiscal year of the report"
    )
    period: str = Field(..., description="Reporting period, e.g., FY, Q1, Q2")

    revenue: int = Field(..., description="Total company revenue")
    cost_of_revenue: int = Field(
        ..., alias="costOfRevenue", description="Total cost of goods sold"
    )
    gross_profit: int = Field(
        ..., alias="grossProfit", description="Revenue minus cost of goods sold"
    )

    research_and_development_expenses: int = Field(
        ..., alias="researchAndDevelopmentExpenses", description="R&D expenses"
    )
    general_and_administrative_expenses: int = Field(
        ...,
        alias="generalAndAdministrativeExpenses",
        description="General and administrative expenses",
    )
    selling_and_marketing_expenses: int = Field(
        ...,
        alias="sellingAndMarketingExpenses",
        description="Selling and marketing expenses",
    )
    selling_general_and_administrative_expenses: int = Field(
        ...,
        alias="sellingGeneralAndAdministrativeExpenses",
        description="Combined selling, general, and administrative expenses",
    )
    other_expenses: int = Field(
        ..., alias="otherExpenses", description="Other miscellaneous expenses"
    )
    operating_expenses: int = Field(
        ..., alias="operatingExpenses", description="Total operating expenses"
    )
    cost_and_expenses: int = Field(
        ..., alias="costAndExpenses", description="Sum of cost and expenses"
    )

    net_interest_income: int = Field(
        ..., alias="netInterestIncome", description="Net interest income"
    )
    interest_income: int = Field(
        ..., alias="interestIncome", description="Interest income"
    )
    interest_expense: int = Field(
        ..., alias="interestExpense", description="Interest expense"
    )

    depreciation_and_amortization: int = Field(
        ...,
        alias="depreciationAndAmortization",
        description="Depreciation and amortization expense",
    )

    ebitda: int = Field(
        ...,
        description="Earnings before interest, taxes, depreciation, and amortization",
    )
    ebit: int = Field(..., description="Earnings before interest and taxes")
    non_operating_income_excluding_interest: int = Field(
        ...,
        alias="nonOperatingIncomeExcludingInterest",
        description="Non-operating income excluding interest",
    )
    operating_income: int = Field(
        ..., alias="operatingIncome", description="Operating income"
    )

    total_other_income_expenses_net: int = Field(
        ...,
        alias="totalOtherIncomeExpensesNet",
        description="Net total of other income/expenses",
    )
    income_before_tax: int = Field(
        ..., alias="incomeBeforeTax", description="Income before taxes"
    )
    income_tax_expense: int = Field(
        ..., alias="incomeTaxExpense", description="Income tax expense"
    )

    net_income_from_continuing_operations: int = Field(
        ...,
        alias="netIncomeFromContinuingOperations",
        description="Net income from continuing operations",
    )
    net_income_from_discontinued_operations: int = Field(
        ...,
        alias="netIncomeFromDiscontinuedOperations",
        description="Net income from discontinued operations",
    )
    other_adjustments_to_net_income: int = Field(
        ...,
        alias="otherAdjustmentsToNetIncome",
        description="Other adjustments to net income",
    )
    net_income: int = Field(..., alias="netIncome", description="Total net income")
    net_income_deductions: int = Field(
        ..., alias="netIncomeDeductions", description="Net income deductions"
    )
    bottom_line_net_income: int = Field(
        ..., alias="bottomLineNetIncome", description="Final net income value"
    )

    eps: float = Field(..., description="Earnings per share (basic)")
    eps_diluted: float = Field(
        ..., alias="epsDiluted", description="Earnings per share (diluted)"
    )
    weighted_average_shs_out: int = Field(
        ...,
        alias="weightedAverageShsOut",
        description="Weighted average shares outstanding (basic)",
    )
    weighted_average_shs_out_dil: int = Field(
        ...,
        alias="weightedAverageShsOutDil",
        description="Weighted average shares outstanding (diluted)",
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


class FMPCompanyBalanceSheet(BaseModel):
    date: date_type = Field(..., description="Date of the financial statement")
    symbol: str = Field(..., description="Ticker symbol of the company")
    reported_currency: str = Field(
        ..., alias="reportedCurrency", description="Currency reported in the statement"
    )
    cik: str = Field(..., description="SEC Central Index Key identifier")
    filing_date: str = Field(
        ..., alias="filingDate", description="Filing date of the report"
    )
    accepted_date: str = Field(
        ..., alias="acceptedDate", description="Accepted date/time by SEC"
    )
    fiscal_year: str = Field(
        ..., alias="fiscalYear", description="Fiscal year of the report"
    )
    period: str = Field(..., description="Reporting period, e.g., FY, Q1, etc.")

    # Assets
    cash_and_cash_equivalents: int = Field(
        ..., alias="cashAndCashEquivalents", description="Cash and equivalents"
    )
    short_term_investments: int = Field(
        ..., alias="shortTermInvestments", description="Short-term investments"
    )
    cash_and_short_term_investments: int = Field(
        ...,
        alias="cashAndShortTermInvestments",
        description="Total cash and short-term investments",
    )
    net_receivables: int = Field(
        ..., alias="netReceivables", description="Net receivables"
    )
    accounts_receivables: int = Field(
        ..., alias="accountsReceivables", description="Accounts receivable"
    )
    other_receivables: int = Field(
        ..., alias="otherReceivables", description="Other receivables"
    )
    inventory: int = Field(..., description="Inventory value")
    prepaids: int = Field(..., description="Prepaid expenses")
    other_current_assets: int = Field(
        ..., alias="otherCurrentAssets", description="Other current assets"
    )
    total_current_assets: int = Field(
        ..., alias="totalCurrentAssets", description="Total current assets"
    )

    property_plant_equipment_net: int = Field(
        ...,
        alias="propertyPlantEquipmentNet",
        description="Net property, plant, and equipment",
    )
    goodwill: int = Field(..., description="Goodwill value")
    intangible_assets: int = Field(
        ..., alias="intangibleAssets", description="Intangible assets"
    )
    goodwill_and_intangible_assets: int = Field(
        ...,
        alias="goodwillAndIntangibleAssets",
        description="Combined goodwill and intangible assets",
    )
    long_term_investments: int = Field(
        ..., alias="longTermInvestments", description="Long-term investments"
    )
    tax_assets: int = Field(..., alias="taxAssets", description="Tax-related assets")
    other_non_current_assets: int = Field(
        ..., alias="otherNonCurrentAssets", description="Other non-current assets"
    )
    total_non_current_assets: int = Field(
        ..., alias="totalNonCurrentAssets", description="Total non-current assets"
    )
    other_assets: int = Field(..., alias="otherAssets", description="Other assets")
    total_assets: int = Field(..., alias="totalAssets", description="Total assets")

    # Liabilities
    total_payables: int = Field(
        ..., alias="totalPayables", description="Total payables"
    )
    account_payables: int = Field(
        ..., alias="accountPayables", description="Accounts payable"
    )
    other_payables: int = Field(
        ..., alias="otherPayables", description="Other payables"
    )
    accrued_expenses: int = Field(
        ..., alias="accruedExpenses", description="Accrued expenses"
    )
    short_term_debt: int = Field(
        ..., alias="shortTermDebt", description="Short-term debt"
    )
    capital_lease_obligations_current: int = Field(
        ...,
        alias="capitalLeaseObligationsCurrent",
        description="Current portion of capital lease obligations",
    )
    tax_payables: int = Field(..., alias="taxPayables", description="Tax payables")
    deferred_revenue: int = Field(
        ..., alias="deferredRevenue", description="Deferred revenue (current)"
    )
    other_current_liabilities: int = Field(
        ..., alias="otherCurrentLiabilities", description="Other current liabilities"
    )
    total_current_liabilities: int = Field(
        ..., alias="totalCurrentLiabilities", description="Total current liabilities"
    )

    long_term_debt: int = Field(..., alias="longTermDebt", description="Long-term debt")
    deferred_revenue_non_current: int = Field(
        ...,
        alias="deferredRevenueNonCurrent",
        description="Deferred revenue (non-current)",
    )
    deferred_tax_liabilities_non_current: int = Field(
        ...,
        alias="deferredTaxLiabilitiesNonCurrent",
        description="Deferred tax liabilities (non-current)",
    )
    other_non_current_liabilities: int = Field(
        ...,
        alias="otherNonCurrentLiabilities",
        description="Other non-current liabilities",
    )
    total_non_current_liabilities: int = Field(
        ...,
        alias="totalNonCurrentLiabilities",
        description="Total non-current liabilities",
    )
    other_liabilities: int = Field(
        ..., alias="otherLiabilities", description="Other liabilities"
    )
    capital_lease_obligations: int = Field(
        ...,
        alias="capitalLeaseObligations",
        description="Total capital lease obligations",
    )
    total_liabilities: int = Field(
        ..., alias="totalLiabilities", description="Total liabilities"
    )

    # Equity
    treasury_stock: int = Field(
        ..., alias="treasuryStock", description="Treasury stock"
    )
    preferred_stock: int = Field(
        ..., alias="preferredStock", description="Preferred stock"
    )
    common_stock: int = Field(
        ..., alias="commonStock", description="Common stock value"
    )
    retained_earnings: int = Field(
        ..., alias="retainedEarnings", description="Retained earnings"
    )
    additional_paid_in_capital: int = Field(
        ..., alias="additionalPaidInCapital", description="Additional paid-in capital"
    )
    accumulated_other_comprehensive_income_loss: int = Field(
        ...,
        alias="accumulatedOtherComprehensiveIncomeLoss",
        description="Accumulated other comprehensive income/loss",
    )
    other_total_stockholders_equity: int = Field(
        ...,
        alias="otherTotalStockholdersEquity",
        description="Other stockholders' equity",
    )
    total_stockholders_equity: int = Field(
        ..., alias="totalStockholdersEquity", description="Total stockholders' equity"
    )
    total_equity: int = Field(..., alias="totalEquity", description="Total equity")
    minority_interest: int = Field(
        ..., alias="minorityInterest", description="Minority interest"
    )

    total_liabilities_and_total_equity: int = Field(
        ...,
        alias="totalLiabilitiesAndTotalEquity",
        description="Total liabilities and equity",
    )
    total_investments: int = Field(
        ..., alias="totalInvestments", description="Total investments"
    )
    total_debt: int = Field(
        ..., alias="totalDebt", description="Total debt (short + long term)"
    )
    net_debt: int = Field(
        ..., alias="netDebt", description="Net debt (total debt - cash)"
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


class FMPCompanyCashFlowStatement(BaseModel):
    date: date_type = Field(..., description="Date of the financial statement")
    symbol: str
    reported_currency: str = Field(alias="reportedCurrency")
    cik: str
    filing_date: str = Field(alias="filingDate")
    accepted_date: str = Field(alias="acceptedDate")
    fiscal_year: str = Field(alias="fiscalYear")
    period: str

    net_income: int = Field(alias="netIncome")
    depreciation_and_amortization: int = Field(alias="depreciationAndAmortization")
    deferred_income_tax: int = Field(alias="deferredIncomeTax")
    stock_based_compensation: int = Field(alias="stockBasedCompensation")
    change_in_working_capital: int = Field(alias="changeInWorkingCapital")
    accounts_receivables: int = Field(alias="accountsReceivables")
    inventory: int
    accounts_payables: int = Field(alias="accountsPayables")
    other_working_capital: int = Field(alias="otherWorkingCapital")
    other_non_cash_items: int = Field(alias="otherNonCashItems")
    net_cash_provided_by_operating_activities: int = Field(
        alias="netCashProvidedByOperatingActivities"
    )

    investments_in_property_plant_and_equipment: int = Field(
        alias="investmentsInPropertyPlantAndEquipment"
    )
    acquisitions_net: int = Field(alias="acquisitionsNet")
    purchases_of_investments: int = Field(alias="purchasesOfInvestments")
    sales_maturities_of_investments: int = Field(alias="salesMaturitiesOfInvestments")
    other_investing_activities: int = Field(alias="otherInvestingActivities")
    net_cash_provided_by_investing_activities: int = Field(
        alias="netCashProvidedByInvestingActivities"
    )

    net_debt_issuance: int = Field(alias="netDebtIssuance")
    long_term_net_debt_issuance: int = Field(alias="longTermNetDebtIssuance")
    short_term_net_debt_issuance: int = Field(alias="shortTermNetDebtIssuance")
    net_stock_issuance: int = Field(alias="netStockIssuance")
    net_common_stock_issuance: int = Field(alias="netCommonStockIssuance")
    common_stock_issuance: int = Field(alias="commonStockIssuance")
    common_stock_repurchased: int = Field(alias="commonStockRepurchased")
    net_preferred_stock_issuance: int = Field(alias="netPreferredStockIssuance")
    net_dividends_paid: int = Field(alias="netDividendsPaid")
    common_dividends_paid: int = Field(alias="commonDividendsPaid")
    preferred_dividends_paid: int = Field(alias="preferredDividendsPaid")
    other_financing_activities: int = Field(alias="otherFinancingActivities")
    net_cash_provided_by_financing_activities: int = Field(
        alias="netCashProvidedByFinancingActivities"
    )

    effect_of_forex_changes_on_cash: int = Field(alias="effectOfForexChangesOnCash")
    net_change_in_cash: int = Field(alias="netChangeInCash")
    cash_at_end_of_period: int = Field(alias="cashAtEndOfPeriod")
    cash_at_beginning_of_period: int = Field(alias="cashAtBeginningOfPeriod")
    operating_cash_flow: int = Field(alias="operatingCashFlow")
    capital_expenditure: int = Field(alias="capitalExpenditure")
    free_cash_flow: int = Field(alias="freeCashFlow")
    income_taxes_paid: int = Field(alias="incomeTaxesPaid")
    interest_paid: int = Field(alias="interestPaid")

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
