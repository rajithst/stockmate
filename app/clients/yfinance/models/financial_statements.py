from datetime import date as date_type
from pydantic import BaseModel, ConfigDict, Field, field_validator


# Mapping from YFinance API keys to database schema fields - Income Statement
YF_INCOME_STATEMENT_MAP = {
    "TotalRevenue": "revenue",
    "OperatingRevenue": "revenue",  # fallback
    "NetInterestIncome": "net_interest_income",
    "InterestIncome": "interest_income",
    "InterestExpense": "interest_expense",
    "TaxProvision": "income_tax_expense",
    "PretaxIncome": "income_before_tax",
    "NetIncome": "net_income",
    "NetIncomeIncludingNoncontrollingEntitlements": "net_income",
    "NetIncomeContinuousOperations": "net_income_from_continuing_operations",
    "NetIncomeFromContinuingOperationNetMinorityInterest": "net_income_from_continuing_operations",
    "NetIncomeCommonStockholders": "bottom_line_net_income",
    "DilutedNIAvailtoComStockholders": "bottom_line_net_income",
    "DilutedEPS": "eps_diluted",
    "BasicEPS": "eps",
    "DilutedAverageShares": "weighted_average_shs_out_dil",
    "BasicAverageShares": "weighted_average_shs_out",
    "SellingGeneralAndAdministration": "selling_general_and_administrative_expenses",
    "GeneralAndAdministrativeExpense": "general_and_administrative_expenses",
    "OtherGandA": "other_expenses",
    "SpecialIncomeCharges": "other_expenses",
    "OtherSpecialCharges": "other_expenses",
    "GainOnSaleOfSecurity": "other_adjustments_to_net_income",
    "MinorityInterests": "net_income_deductions",
}

# Mapping from YFinance API keys to database schema fields - Balance Sheet
YF_BALANCE_SHEET_MAP = {
    "TotalAssets": "total_assets",
    "CashAndCashEquivalents": "cash_and_cash_equivalents",
    "CashCashEquivalentsAndFederalFundsSold": "cash_and_cash_equivalents",
    "InvestmentsAndAdvances": "long_term_investments",
    "Goodwill": "goodwill",
    "OtherIntangibleAssets": "intangible_assets",
    "GoodwillAndOtherIntangibleAssets": "goodwill_and_intangible_assets",
    "NetPPE": "property_plant_equipment_net",
    "TotalDebt": "total_debt",
    "LongTermDebt": "long_term_debt",
    "CurrentDebt": "short_term_debt",
    "Payables": "account_payables",
    "OtherPayable": "other_payables",
    "PayablesAndAccruedExpenses": "accrued_expenses",
    "TotalLiabilitiesNetMinorityInterest": "total_liilities",
    "RetainedEarnings": "retained_earnings",
    "AdditionalPaidInCapital": "additional_paid_in_capital",
    "TreasuryStock": "treasury_stock",
    "StockholdersEquity": "total_stockholders_equity",
    "TotalEquityGrossMinorityInterest": "total_equity",
    "MinorityInterest": "minority_interest",
    "LongTermDebtAndCapitalLeaseObligation": "capital_lease_obligations",
    "CurrentDebtAndCapitalLeaseObligation": "capital_lease_obligations_current",
}

# Mapping from YFinance API keys to database schema fields - Cash Flow
YF_CASHFLOW_MAP = {
    "FreeCashFlow": "free_cash_flow",
    "OperatingCashFlow": "operating_cash_flow",
    "CapitalExpenditure": "capital_expenditure",
    "IncomeTaxPaidSupplementalData": "income_taxes_paid",
    "InterestPaidSupplementalData": "interest_paid",
    "EndCashPosition": "cash_at_end_of_period",
    "BeginningCashPosition": "cash_at_beginning_of_period",
    "EffectOfExchangeRateChanges": "effect_of_forex_changes_on_cash",
    "ChangesInCash": "net_change_in_cash",
    "CashFlowFromContinuingOperatingActivities": "net_cash_provided_by_operating_activities",
    "CashFlowFromContinuingInvestingActivities": "net_cash_provided_by_investing_activities",
    "CashFlowFromContinuingFinancingActivities": "net_cash_provided_by_financing_activities",
    "PurchaseOfPPE": "investments_in_property_plant_and_equipment",
    "NetBusinessPurchaseAndSale": "acquisitions_net",
    "PurchasesOfInvestments": "purchases_of_investments",
    "SalesMaturitiesOfInvestments": "sales_maturities_of_investments",
    "NetOtherInvestingChanges": "other_investing_activities",
    "NetIssuancePaymentsOfDebt": "net_debt_issuance",
    "NetLongTermDebtIssuance": "long_term_net_debt_issuance",
    "NetShortTermDebtIssuance": "short_term_net_debt_issuance",
    "NetCommonStockIssuance": "net_common_stock_issuance",
    "CommonStockIssuance": "common_stock_issuance",
    "CommonStockPayments": "common_stock_repurchased",
    "CashDividendsPaid": "net_dividends_paid",
    "CommonStockDividendPaid": "common_dividends_paid",
    "NetOtherFinancingChanges": "other_financing_activities",
    "NetIncomeFromContinuingOperations": "net_income",
}


class YFinanceIncomeStatement(BaseModel):
    """Income statement data from yfinance

    Fields mapped from YFinance API response using YF_TO_DB_MAP.
    Unmapped fields default to 0.0.
    """

    # Required fields (no alias - set directly)
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

    # Revenue fields (mapped from YFinance)
    revenue: float = Field(
        default=0.0, alias="TotalRevenue", description="Total company revenue"
    )
    cost_of_revenue: float = Field(default=0.0, description="Total cost of goods sold")
    gross_profit: float = Field(
        default=0.0, description="Revenue minus cost of goods sold"
    )

    # Expense fields (mostly default to 0)
    research_and_development_expenses: float = Field(
        default=0.0, description="R&D expenses"
    )
    general_and_administrative_expenses: float = Field(
        default=0.0,
        alias="GeneralAndAdministrativeExpense",
        description="General and administrative expenses",
    )
    selling_and_marketing_expenses: float = Field(
        default=0.0,
        description="Selling and marketing expenses",
    )
    selling_general_and_administrative_expenses: float = Field(
        default=0.0,
        alias="SellingGeneralAndAdministration",
        description="Combined selling, general, and administrative expenses",
    )
    other_expenses: float = Field(
        default=0.0, alias="OtherGandA", description="Other miscellaneous expenses"
    )
    operating_expenses: float = Field(
        default=0.0, description="Total operating expenses"
    )
    cost_and_expenses: float = Field(
        default=0.0, description="Sum of cost and expenses"
    )

    # Interest fields (mapped from YFinance)
    net_interest_income: float = Field(
        default=0.0, alias="NetInterestIncome", description="Net interest income"
    )
    interest_income: float = Field(
        default=0.0, alias="InterestIncome", description="Interest income"
    )
    interest_expense: float = Field(
        default=0.0, alias="InterestExpense", description="Interest expense"
    )

    # Depreciation and amortization (default to 0)
    depreciation_and_amortization: float = Field(
        default=0.0,
        description="Depreciation and amortization expense",
    )

    # EBITDA and EBIT fields (default to 0)
    ebitda: float = Field(
        default=0.0,
        description="Earnings before interest, taxes, depreciation, and amortization",
    )
    ebit: float = Field(default=0.0, description="Earnings before interest and taxes")
    non_operating_income_excluding_interest: float = Field(
        default=0.0,
        description="Non-operating income excluding interest",
    )
    operating_income: float = Field(default=0.0, description="Operating income")

    # Income/Tax fields (default to 0)
    total_other_income_expenses_net: float = Field(
        default=0.0,
        description="Net total of other income/expenses",
    )
    income_before_tax: float = Field(
        default=0.0, alias="PretaxIncome", description="Income before taxes"
    )
    income_tax_expense: float = Field(
        default=0.0, alias="TaxProvision", description="Income tax expense"
    )

    # Net income fields (mapped from YFinance)
    net_income_from_continuing_operations: float = Field(
        default=0.0,
        alias="NetIncomeContinuousOperations",
        description="Net income from continuing operations",
    )
    net_income_from_discontinued_operations: float = Field(
        default=0.0,
        description="Net income from discontinued operations",
    )
    other_adjustments_to_net_income: float = Field(
        default=0.0,
        alias="GainOnSaleOfSecurity",
        description="Other adjustments to net income",
    )
    net_income: float = Field(
        default=0.0, alias="NetIncome", description="Total net income"
    )
    net_income_deductions: float = Field(
        default=0.0, alias="MinorityInterests", description="Net income deductions"
    )
    bottom_line_net_income: float = Field(
        default=0.0,
        alias="NetIncomeCommonStockholders",
        description="Final net income value",
    )

    # EPS fields (mapped from YFinance)
    eps: float = Field(
        default=0.0, alias="BasicEPS", description="Earnings per share (basic)"
    )
    eps_diluted: float = Field(
        default=0.0, alias="DilutedEPS", description="Earnings per share (diluted)"
    )
    weighted_average_shs_out: float = Field(
        default=0.0,
        alias="BasicAverageShares",
        description="Weighted average shares outstanding (basic)",
    )
    weighted_average_shs_out_dil: float = Field(
        default=0.0,
        alias="DilutedAverageShares",
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


class YFinanceBalanceSheet(BaseModel):
    """Balance sheet data from yfinance

    Fields mapped from YFinance API response using YF_BALANCE_SHEET_MAP.
    Unmapped fields default to 0.0.
    """

    # Required fields (no alias - set directly)
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

    # Assets - Cash and Investments
    cash_and_cash_equivalents: float = Field(
        default=0.0, alias="CashAndCashEquivalents", description="Cash and equivalents"
    )
    short_term_investments: float = Field(
        default=0.0, description="Short-term investments"
    )
    cash_and_short_term_investments: float = Field(
        default=0.0,
        description="Total cash and short-term investments",
    )

    # Assets - Receivables
    net_receivables: float = Field(default=0.0, description="Net receivables")
    accounts_receivables: float = Field(default=0.0, description="Accounts receivable")
    other_receivables: float = Field(default=0.0, description="Other receivables")

    # Assets - Current
    inventory: float = Field(default=0.0, description="Inventory value")
    prepaids: float = Field(default=0.0, description="Prepaid expenses")
    other_current_assets: float = Field(default=0.0, description="Other current assets")
    total_current_assets: float = Field(default=0.0, description="Total current assets")

    # Assets - Long-term
    property_plant_equipment_net: float = Field(
        default=0.0,
        alias="NetPPE",
        description="Net property, plant, and equipment",
    )
    goodwill: float = Field(default=0.0, alias="Goodwill", description="Goodwill value")
    intangible_assets: float = Field(
        default=0.0, alias="OtherIntangibleAssets", description="Intangible assets"
    )
    goodwill_and_intangible_assets: float = Field(
        default=0.0,
        alias="GoodwillAndOtherIntangibleAssets",
        description="Combined goodwill and intangible assets",
    )
    long_term_investments: float = Field(
        default=0.0, alias="InvestmentsAndAdvances", description="Long-term investments"
    )
    tax_assets: float = Field(default=0.0, description="Tax-related assets")
    other_non_current_assets: float = Field(
        default=0.0, description="Other non-current assets"
    )
    total_non_current_assets: float = Field(
        default=0.0, description="Total non-current assets"
    )
    other_assets: float = Field(default=0.0, description="Other assets")

    # Total Assets (mapped)
    total_assets: float = Field(
        default=0.0, alias="TotalAssets", description="Total assets"
    )

    # Liabilities - Current
    total_payables: float = Field(default=0.0, description="Total payables")
    account_payables: float = Field(
        default=0.0, alias="Payables", description="Accounts payable"
    )
    other_payables: float = Field(
        default=0.0, alias="OtherPayable", description="Other payables"
    )
    accrued_expenses: float = Field(
        default=0.0, alias="PayablesAndAccruedExpenses", description="Accrued expenses"
    )
    short_term_debt: float = Field(
        default=0.0, alias="CurrentDebt", description="Short-term debt"
    )
    capital_lease_obligations_current: float = Field(
        default=0.0,
        alias="CurrentDebtAndCapitalLeaseObligation",
        description="Current portion of capital lease obligations",
    )
    tax_payables: float = Field(default=0.0, description="Tax payables")
    deferred_revenue: float = Field(
        default=0.0, description="Deferred revenue (current)"
    )
    other_current_liabilities: float = Field(
        default=0.0, description="Other current liabilities"
    )
    total_current_liabilities: float = Field(
        default=0.0, description="Total current liabilities"
    )

    # Liabilities - Long-term
    long_term_debt: float = Field(
        default=0.0, alias="LongTermDebt", description="Long-term debt"
    )
    deferred_revenue_non_current: float = Field(
        default=0.0,
        description="Deferred revenue (non-current)",
    )
    deferred_tax_liabilities_non_current: float = Field(
        default=0.0,
        description="Deferred tax liabilities (non-current)",
    )
    other_non_current_liabilities: float = Field(
        default=0.0,
        description="Other non-current liabilities",
    )
    total_non_current_liabilities: float = Field(
        default=0.0,
        description="Total non-current liabilities",
    )
    other_liabilities: float = Field(default=0.0, description="Other liabilities")
    capital_lease_obligations: float = Field(
        default=0.0,
        alias="LongTermDebtAndCapitalLeaseObligation",
        description="Total capital lease obligations",
    )
    total_liilities: float = Field(
        default=0.0,
        alias="TotalLiabilitiesNetMinorityInterest",
        description="Total liabilities",
    )

    # Equity
    treasury_stock: float = Field(
        default=0.0, alias="TreasuryStock", description="Treasury stock"
    )
    preferred_stock: float = Field(default=0.0, description="Preferred stock")
    common_stock: float = Field(default=0.0, description="Common stock value")
    retained_earnings: float = Field(
        default=0.0, alias="RetainedEarnings", description="Retained earnings"
    )
    additional_paid_in_capital: float = Field(
        default=0.0,
        alias="AdditionalPaidInCapital",
        description="Additional paid-in capital",
    )
    accumulated_other_comprehensive_income_loss: float = Field(
        default=0.0,
        description="Accumulated other comprehensive income/loss",
    )
    other_total_stockholders_equity: float = Field(
        default=0.0,
        description="Other stockholders' equity",
    )
    total_stockholders_equity: float = Field(
        default=0.0,
        alias="StockholdersEquity",
        description="Total stockholders' equity",
    )
    total_equity: float = Field(
        default=0.0,
        alias="TotalEquityGrossMinorityInterest",
        description="Total equity",
    )
    minority_interest: float = Field(
        default=0.0, alias="MinorityInterest", description="Minority interest"
    )

    # Summary fields
    total_liabilities_and_total_equity: float = Field(
        default=0.0,
        description="Total liabilities and equity",
    )
    total_investments: float = Field(default=0.0, description="Total investments")
    total_debt: float = Field(
        default=0.0, alias="TotalDebt", description="Total debt (short + long term)"
    )
    net_debt: float = Field(default=0.0, description="Net debt (total debt - cash)")

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


class YFinanceCashFlow(BaseModel):
    """Cash flow statement data from yfinance

    Fields mapped from YFinance API response using YF_CASHFLOW_MAP.
    Unmapped fields default to 0.0.
    """

    # Required fields (no alias - set directly)
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

    # Operating Activities (mapped from YFinance)
    net_income: float = Field(
        default=0.0,
        alias="NetIncomeFromContinuingOperations",
        description="Net income from continuing operations",
    )
    depreciation_and_amortization: float = Field(
        default=0.0, description="Depreciation and amortization expense"
    )
    deferred_income_tax: float = Field(default=0.0, description="Deferred income tax")
    stock_based_compensation: float = Field(
        default=0.0, description="Stock-based compensation"
    )
    change_in_working_capital: float = Field(
        default=0.0, description="Change in working capital"
    )
    accounts_receivables: float = Field(
        default=0.0, description="Change in accounts receivables"
    )
    inventory: float = Field(default=0.0, description="Change in inventory")
    accounts_payables: float = Field(
        default=0.0, description="Change in accounts payables"
    )
    other_working_capital: float = Field(
        default=0.0, description="Other changes in working capital"
    )
    other_non_cash_items: float = Field(default=0.0, description="Other non-cash items")
    net_cash_provided_by_operating_activities: float = Field(
        default=0.0,
        alias="CashFlowFromContinuingOperatingActivities",
        description="Net cash from operating activities",
    )

    # Investing Activities (mapped from YFinance)
    investments_in_property_plant_and_equipment: float = Field(
        default=0.0, alias="PurchaseOfPPE", description="Investments in PP&E"
    )
    acquisitions_net: float = Field(
        default=0.0, alias="NetBusinessPurchaseAndSale", description="Net acquisitions"
    )
    purchases_of_investments: float = Field(
        default=0.0,
        alias="PurchasesOfInvestments",
        description="Purchases of investments",
    )
    sales_maturities_of_investments: float = Field(
        default=0.0,
        alias="SalesMaturitiesOfInvestments",
        description="Sales and maturities of investments",
    )
    other_investing_activities: float = Field(
        default=0.0,
        alias="NetOtherInvestingChanges",
        description="Other investing activities",
    )
    net_cash_provided_by_investing_activities: float = Field(
        default=0.0,
        alias="CashFlowFromContinuingInvestingActivities",
        description="Net cash from investing activities",
    )

    # Financing Activities (mapped from YFinance)
    net_debt_issuance: float = Field(
        default=0.0, alias="NetIssuancePaymentsOfDebt", description="Net debt issuance"
    )
    long_term_net_debt_issuance: float = Field(
        default=0.0,
        alias="NetLongTermDebtIssuance",
        description="Long-term net debt issuance",
    )
    short_term_net_debt_issuance: float = Field(
        default=0.0,
        alias="NetShortTermDebtIssuance",
        description="Short-term net debt issuance",
    )
    net_stock_issuance: float = Field(default=0.0, description="Net stock issuance")
    net_common_stock_issuance: float = Field(
        default=0.0,
        alias="NetCommonStockIssuance",
        description="Net common stock issuance",
    )
    common_stock_issuance: float = Field(
        default=0.0, alias="CommonStockIssuance", description="Common stock issuance"
    )
    common_stock_repurchased: float = Field(
        default=0.0, alias="CommonStockPayments", description="Common stock repurchased"
    )
    net_preferred_stock_issuance: float = Field(
        default=0.0, description="Net preferred stock issuance"
    )
    net_dividends_paid: float = Field(
        default=0.0, alias="CashDividendsPaid", description="Net dividends paid"
    )
    common_dividends_paid: float = Field(
        default=0.0,
        alias="CommonStockDividendPaid",
        description="Common stock dividends paid",
    )
    preferred_dividends_paid: float = Field(
        default=0.0, description="Preferred dividends paid"
    )
    other_financing_activities: float = Field(
        default=0.0,
        alias="NetOtherFinancingChanges",
        description="Other financing activities",
    )
    net_cash_provided_by_financing_activities: float = Field(
        default=0.0,
        alias="CashFlowFromContinuingFinancingActivities",
        description="Net cash from financing activities",
    )

    # Cash flows and reconciliation (mapped from YFinance)
    effect_of_forex_changes_on_cash: float = Field(
        default=0.0,
        alias="EffectOfExchangeRateChanges",
        description="Effect of exchange rate changes on cash",
    )
    net_change_in_cash: float = Field(
        default=0.0, alias="ChangesInCash", description="Net change in cash"
    )
    cash_at_end_of_period: float = Field(
        default=0.0, alias="EndCashPosition", description="Cash at end of period"
    )
    cash_at_beginning_of_period: float = Field(
        default=0.0,
        alias="BeginningCashPosition",
        description="Cash at beginning of period",
    )

    # Summary metrics (mapped from YFinance)
    operating_cash_flow: float = Field(
        default=0.0, alias="OperatingCashFlow", description="Operating cash flow"
    )
    capital_expenditure: float = Field(
        default=0.0, alias="CapitalExpenditure", description="Capital expenditure"
    )
    free_cash_flow: float = Field(
        default=0.0, alias="FreeCashFlow", description="Free cash flow"
    )
    income_taxes_paid: float = Field(
        default=0.0,
        alias="IncomeTaxPaidSupplementalData",
        description="Income taxes paid",
    )
    interest_paid: float = Field(
        default=0.0, alias="InterestPaidSupplementalData", description="Interest paid"
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
