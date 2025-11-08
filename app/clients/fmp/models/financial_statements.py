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

    revenue: float = Field(..., description="Total company revenue")
    cost_of_revenue: float = Field(
        ..., alias="costOfRevenue", description="Total cost of goods sold"
    )
    gross_profit: float = Field(
        ..., alias="grossProfit", description="Revenue minus cost of goods sold"
    )

    research_and_development_expenses: float = Field(
        ..., alias="researchAndDevelopmentExpenses", description="R&D expenses"
    )
    general_and_administrative_expenses: float = Field(
        ...,
        alias="generalAndAdministrativeExpenses",
        description="General and administrative expenses",
    )
    selling_and_marketing_expenses: float = Field(
        ...,
        alias="sellingAndMarketingExpenses",
        description="Selling and marketing expenses",
    )
    selling_general_and_administrative_expenses: float = Field(
        ...,
        alias="sellingGeneralAndAdministrativeExpenses",
        description="Combined selling, general, and administrative expenses",
    )
    other_expenses: float = Field(
        ..., alias="otherExpenses", description="Other miscellaneous expenses"
    )
    operating_expenses: float = Field(
        ..., alias="operatingExpenses", description="Total operating expenses"
    )
    cost_and_expenses: float = Field(
        ..., alias="costAndExpenses", description="Sum of cost and expenses"
    )

    net_interest_income: float = Field(
        ..., alias="netInterestIncome", description="Net interest income"
    )
    interest_income: float = Field(
        ..., alias="interestIncome", description="Interest income"
    )
    interest_expense: float = Field(
        ..., alias="interestExpense", description="Interest expense"
    )

    depreciation_and_amortization: float = Field(
        ...,
        alias="depreciationAndAmortization",
        description="Depreciation and amortization expense",
    )

    ebitda: float = Field(
        ...,
        description="Earnings before interest, taxes, depreciation, and amortization",
    )
    ebit: float = Field(..., description="Earnings before interest and taxes")
    non_operating_income_excluding_interest: float = Field(
        ...,
        alias="nonOperatingIncomeExcludingInterest",
        description="Non-operating income excluding interest",
    )
    operating_income: float = Field(
        ..., alias="operatingIncome", description="Operating income"
    )

    total_other_income_expenses_net: float = Field(
        ...,
        alias="totalOtherIncomeExpensesNet",
        description="Net total of other income/expenses",
    )
    income_before_tax: float = Field(
        ..., alias="incomeBeforeTax", description="Income before taxes"
    )
    income_tax_expense: float = Field(
        ..., alias="incomeTaxExpense", description="Income tax expense"
    )

    net_income_from_continuing_operations: float = Field(
        ...,
        alias="netIncomeFromContinuingOperations",
        description="Net income from continuing operations",
    )
    net_income_from_discontinued_operations: float = Field(
        ...,
        alias="netIncomeFromDiscontinuedOperations",
        description="Net income from discontinued operations",
    )
    other_adjustments_to_net_income: float = Field(
        ...,
        alias="otherAdjustmentsToNetIncome",
        description="Other adjustments to net income",
    )
    net_income: float = Field(..., alias="netIncome", description="Total net income")
    net_income_deductions: float = Field(
        ..., alias="netIncomeDeductions", description="Net income deductions"
    )
    bottom_line_net_income: float = Field(
        ..., alias="bottomLineNetIncome", description="Final net income value"
    )

    eps: float = Field(..., description="Earnings per share (basic)")
    eps_diluted: float = Field(
        ..., alias="epsDiluted", description="Earnings per share (diluted)"
    )
    weighted_average_shs_out: float = Field(
        ...,
        alias="weightedAverageShsOut",
        description="Weighted average shares outstanding (basic)",
    )
    weighted_average_shs_out_dil: float = Field(
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
    cash_and_cash_equivalents: float = Field(
        ..., alias="cashAndCashEquivalents", description="Cash and equivalents"
    )
    short_term_investments: float = Field(
        ..., alias="shortTermInvestments", description="Short-term investments"
    )
    cash_and_short_term_investments: float = Field(
        ...,
        alias="cashAndShortTermInvestments",
        description="Total cash and short-term investments",
    )
    net_receivables: float = Field(
        ..., alias="netReceivables", description="Net receivables"
    )
    accounts_receivables: float = Field(
        ..., alias="accountsReceivables", description="Accounts receivable"
    )
    other_receivables: float = Field(
        ..., alias="otherReceivables", description="Other receivables"
    )
    inventory: float = Field(..., description="Inventory value")
    prepaids: float = Field(..., description="Prepaid expenses")
    other_current_assets: float = Field(
        ..., alias="otherCurrentAssets", description="Other current assets"
    )
    total_current_assets: float = Field(
        ..., alias="totalCurrentAssets", description="Total current assets"
    )

    property_plant_equipment_net: float = Field(
        ...,
        alias="propertyPlantEquipmentNet",
        description="Net property, plant, and equipment",
    )
    goodwill: float = Field(..., description="Goodwill value")
    intangible_assets: float = Field(
        ..., alias="intangibleAssets", description="Intangible assets"
    )
    goodwill_and_intangible_assets: float = Field(
        ...,
        alias="goodwillAndIntangibleAssets",
        description="Combined goodwill and intangible assets",
    )
    long_term_investments: float = Field(
        ..., alias="longTermInvestments", description="Long-term investments"
    )
    tax_assets: float = Field(..., alias="taxAssets", description="Tax-related assets")
    other_non_current_assets: float = Field(
        ..., alias="otherNonCurrentAssets", description="Other non-current assets"
    )
    total_non_current_assets: float = Field(
        ..., alias="totalNonCurrentAssets", description="Total non-current assets"
    )
    other_assets: float = Field(..., alias="otherAssets", description="Other assets")
    total_assets: float = Field(..., alias="totalAssets", description="Total assets")

    # Liabilities
    total_payables: float = Field(
        ..., alias="totalPayables", description="Total payables"
    )
    account_payables: float = Field(
        ..., alias="accountPayables", description="Accounts payable"
    )
    other_payables: float = Field(
        ..., alias="otherPayables", description="Other payables"
    )
    accrued_expenses: float = Field(
        ..., alias="accruedExpenses", description="Accrued expenses"
    )
    short_term_debt: float = Field(
        ..., alias="shortTermDebt", description="Short-term debt"
    )
    capital_lease_obligations_current: float = Field(
        ...,
        alias="capitalLeaseObligationsCurrent",
        description="Current portion of capital lease obligations",
    )
    tax_payables: float = Field(..., alias="taxPayables", description="Tax payables")
    deferred_revenue: float = Field(
        ..., alias="deferredRevenue", description="Deferred revenue (current)"
    )
    other_current_liabilities: float = Field(
        ..., alias="otherCurrentLiabilities", description="Other current liabilities"
    )
    total_current_liabilities: float = Field(
        ..., alias="totalCurrentLiabilities", description="Total current liabilities"
    )

    long_term_debt: float = Field(
        ..., alias="longTermDebt", description="Long-term debt"
    )
    deferred_revenue_non_current: float = Field(
        ...,
        alias="deferredRevenueNonCurrent",
        description="Deferred revenue (non-current)",
    )
    deferred_tax_liabilities_non_current: float = Field(
        ...,
        alias="deferredTaxLiabilitiesNonCurrent",
        description="Deferred tax liabilities (non-current)",
    )
    other_non_current_liabilities: float = Field(
        ...,
        alias="otherNonCurrentLiabilities",
        description="Other non-current liabilities",
    )
    total_non_current_liabilities: float = Field(
        ...,
        alias="totalNonCurrentLiabilities",
        description="Total non-current liabilities",
    )
    other_liabilities: float = Field(
        ..., alias="otherLiabilities", description="Other liabilities"
    )
    capital_lease_obligations: float = Field(
        ...,
        alias="capitalLeaseObligations",
        description="Total capital lease obligations",
    )
    total_liabilities: float = Field(
        ..., alias="totalLiabilities", description="Total liabilities"
    )

    # Equity
    treasury_stock: float = Field(
        ..., alias="treasuryStock", description="Treasury stock"
    )
    preferred_stock: float = Field(
        ..., alias="preferredStock", description="Preferred stock"
    )
    common_stock: float = Field(
        ..., alias="commonStock", description="Common stock value"
    )
    retained_earnings: float = Field(
        ..., alias="retainedEarnings", description="Retained earnings"
    )
    additional_paid_in_capital: float = Field(
        ..., alias="additionalPaidInCapital", description="Additional paid-in capital"
    )
    accumulated_other_comprehensive_income_loss: float = Field(
        ...,
        alias="accumulatedOtherComprehensiveIncomeLoss",
        description="Accumulated other comprehensive income/loss",
    )
    other_total_stockholders_equity: float = Field(
        ...,
        alias="otherTotalStockholdersEquity",
        description="Other stockholders' equity",
    )
    total_stockholders_equity: float = Field(
        ..., alias="totalStockholdersEquity", description="Total stockholders' equity"
    )
    total_equity: float = Field(..., alias="totalEquity", description="Total equity")
    minority_interest: float = Field(
        ..., alias="minorityInterest", description="Minority interest"
    )

    total_liabilities_and_total_equity: float = Field(
        ...,
        alias="totalLiabilitiesAndTotalEquity",
        description="Total liabilities and equity",
    )
    total_investments: float = Field(
        ..., alias="totalInvestments", description="Total investments"
    )
    total_debt: float = Field(
        ..., alias="totalDebt", description="Total debt (short + long term)"
    )
    net_debt: float = Field(
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

    net_income: float = Field(alias="netIncome")
    depreciation_and_amortization: float = Field(alias="depreciationAndAmortization")
    deferred_income_tax: float = Field(alias="deferredIncomeTax")
    stock_based_compensation: float = Field(alias="stockBasedCompensation")
    change_in_working_capital: float = Field(alias="changeInWorkingCapital")
    accounts_receivables: float = Field(alias="accountsReceivables")
    inventory: float = Field(alias="inventory")
    accounts_payables: float = Field(alias="accountsPayables")
    other_working_capital: float = Field(alias="otherWorkingCapital")
    other_non_cash_items: float = Field(alias="otherNonCashItems")
    net_cash_provided_by_operating_activities: float = Field(
        alias="netCashProvidedByOperatingActivities"
    )

    investments_in_property_plant_and_equipment: float = Field(
        alias="investmentsInPropertyPlantAndEquipment"
    )
    acquisitions_net: float = Field(alias="acquisitionsNet")
    purchases_of_investments: float = Field(alias="purchasesOfInvestments")
    sales_maturities_of_investments: float = Field(alias="salesMaturitiesOfInvestments")
    other_investing_activities: float = Field(alias="otherInvestingActivities")
    net_cash_provided_by_investing_activities: float = Field(
        alias="netCashProvidedByInvestingActivities"
    )

    net_debt_issuance: float = Field(alias="netDebtIssuance")
    long_term_net_debt_issuance: float = Field(alias="longTermNetDebtIssuance")
    short_term_net_debt_issuance: float = Field(alias="shortTermNetDebtIssuance")
    net_stock_issuance: float = Field(alias="netStockIssuance")
    net_common_stock_issuance: float = Field(alias="netCommonStockIssuance")
    common_stock_issuance: float = Field(alias="commonStockIssuance")
    common_stock_repurchased: float = Field(alias="commonStockRepurchased")
    net_preferred_stock_issuance: float = Field(alias="netPreferredStockIssuance")
    net_dividends_paid: float = Field(alias="netDividendsPaid")
    common_dividends_paid: float = Field(alias="commonDividendsPaid")
    preferred_dividends_paid: float = Field(alias="preferredDividendsPaid")
    other_financing_activities: float = Field(alias="otherFinancingActivities")
    net_cash_provided_by_financing_activities: float = Field(
        alias="netCashProvidedByFinancingActivities"
    )

    effect_of_forex_changes_on_cash: float = Field(alias="effectOfForexChangesOnCash")
    net_change_in_cash: float = Field(alias="netChangeInCash")
    cash_at_end_of_period: float = Field(alias="cashAtEndOfPeriod")
    cash_at_beginning_of_period: float = Field(alias="cashAtBeginningOfPeriod")
    operating_cash_flow: float = Field(alias="operatingCashFlow")
    capital_expenditure: float = Field(alias="capitalExpenditure")
    free_cash_flow: float = Field(alias="freeCashFlow")
    income_taxes_paid: float = Field(alias="incomeTaxesPaid")
    interest_paid: float = Field(alias="interestPaid")

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
