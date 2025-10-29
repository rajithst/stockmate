from logging import getLogger
import re
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.db.models import Company
from app.repositories.company_repo import CompanyRepository
from app.repositories.financial_repo import FinancialRepository
from app.repositories.metrics_repo import MetricsRepository
from app.schemas.balance_sheet import CompanyBalanceSheetWrite
from app.schemas.cashflow import (
    CompanyCashFlowStatementWrite,
)
from app.schemas.financial_health import (
    CompanyFinancialHealthRead,
    CompanyFinancialHealthWrite,
)
from app.schemas.income_statement import (
    CompanyIncomeStatementWrite,
)

logger = getLogger(__name__)

BENCHMARKS_INSIGHTS = {
    "Gross Profit Margin": {
        "operator": ">",
        "threshold": 40,
        "unit": "%",
        "insight": "Indicates strong product margins and pricing power.",
    },
    "Operating Margin (EBIT)": {
        "operator": ">",
        "threshold": 20,
        "unit": "%",
        "insight": "Shows operational efficiency and cost control.",
    },
    "Net Profit Margin": {
        "operator": ">",
        "threshold": 15,
        "unit": "%",
        "insight": "Reflects overall profitability after all expenses.",
    },
    "ROA (Return on Assets)": {
        "operator": ">",
        "threshold": 10,
        "unit": "%",
        "insight": "Measures how efficiently assets generate profit.",
    },
    "ROE (Return on Equity)": {
        "operator": ">",
        "threshold": 15,
        "unit": "%",
        "insight": "Shows how well equity is used to generate returns.",
    },
    "ROIC (Return on Invested Capital)": {
        "operator": ">",
        "threshold": 10,
        "unit": "%",
        "insight": "Indicates efficiency in using capital for returns.",
    },
    "Asset Turnover": {
        "operator": "~",
        "threshold": 1.0,
        "unit": "×",
        "insight": "Shows how efficiently assets are used to generate sales.",
    },
    "Inventory Turnover": {
        "operator": ">",
        "threshold": 10,
        "unit": "×",
        "insight": "Measures how quickly inventory is sold and replaced.",
    },
    "Receivables Turnover": {
        "operator": "range",
        "low": 5,
        "high": 7,
        "unit": "×",
        "insight": "Indicates effectiveness in collecting receivables.",
    },
    "Payables Turnover": {
        "operator": "range",
        "low": 3,
        "high": 6,
        "unit": "×",
        "insight": "Shows how quickly payables are paid to suppliers.",
    },
    "Cash Conversion Cycle": {
        "operator": "<=",
        "threshold": 0,
        "unit": "days",
        "insight": "Measures time to convert investments into cash.",
    },
    "Current Ratio": {
        "operator": "range",
        "low": 1.0,
        "high": 2.0,
        "unit": "",
        "insight": "Assesses ability to cover short-term obligations.",
    },
    "Quick Ratio": {
        "operator": ">=",
        "threshold": 1.0,
        "unit": "",
        "insight": "Evaluates liquidity excluding inventory.",
    },
    "Cash Ratio": {
        "operator": ">=",
        "threshold": 0.2,
        "unit": "",
        "insight": "Measures ability to pay short-term obligations with cash.",
    },
    "Debt-to-Equity": {
        "operator": "<",
        "threshold": 2.0,
        "unit": "",
        "insight": "Shows leverage and financial risk.",
    },
    "Debt-to-Assets": {
        "operator": "<",
        "threshold": 0.5,
        "unit": "",
        "insight": "Indicates proportion of assets financed by debt.",
    },
    "Interest Coverage": {
        "operator": ">",
        "threshold": 3,
        "unit": "",
        "insight": "Assesses ability to cover interest expenses.",
    },
    "Debt Service Coverage": {
        "operator": ">",
        "threshold": 2.0,
        "unit": "",
        "insight": "Measures ability to service debt from operations.",
    },
    "Operating Cash Flow / Sales": {
        "operator": ">",
        "threshold": 20,
        "unit": "%",
        "insight": "Shows cash generation from core operations.",
    },
    "Free Cash Flow Margin (FCF/Sales)": {
        "operator": ">",
        "threshold": 10,
        "unit": "%",
        "insight": "Indicates efficiency in generating free cash flow.",
    },
    "CapEx / OCF": {
        "operator": "<",
        "threshold": 20,
        "unit": "%",
        "insight": "Measures reinvestment needs relative to operating cash flow.",
    },
    "FCF Coverage Ratio": {
        "operator": ">",
        "threshold": 0.8,
        "unit": "",
        "insight": "Shows conversion of operating cash flow to free cash flow.",
    },
    "Dividend Payout Ratio": {
        "operator": "<",
        "threshold": 50,
        "unit": "%",
        "insight": "Indicates sustainability of dividend payments.",
    },
    "P/E Ratio (Trailing)": {
        "operator": "range",
        "low": 15,
        "high": 25,
        "unit": "",
        "insight": "Compares price to earnings; lower is generally better.",
    },
    "P/S Ratio": {
        "operator": "<",
        "threshold": 5.0,
        "unit": "",
        "insight": "Compares price to sales; lower suggests undervaluation.",
    },
    "P/B Ratio": {
        "operator": "<",
        "threshold": 5.0,
        "unit": "",
        "insight": "Compares price to book value; lower is typically better.",
    },
    "EV/EBITDA": {
        "operator": "<",
        "threshold": 15,
        "unit": "",
        "insight": "Compares enterprise value to EBITDA; lower is preferable.",
    },
    "Earnings Yield": {
        "operator": ">",
        "threshold": 5,
        "unit": "%",
        "insight": "Inverse of P/E; higher yield is better.",
    },
    "FCF Yield": {
        "operator": ">",
        "threshold": 5,
        "unit": "%",
        "insight": "Shows free cash flow relative to market cap; higher is better.",
    },
    "R&D / Revenue": {
        "operator": "range",
        "low": 5,
        "high": 10,
        "unit": "%",
        "insight": "Indicates investment in innovation.",
    },
    "CapEx / Revenue": {
        "operator": "range",
        "low": 3,
        "high": 6,
        "unit": "%",
        "insight": "Shows capital spending efficiency.",
    },
    "PEG Ratio": {
        "operator": "~",
        "threshold": 1,
        "unit": "",
        "insight": "Compares P/E to growth; ~1 is considered fair value.",
    },
    "Dividend Yield": {
        "operator": "range",
        "low": 1,
        "high": 3,
        "unit": "%",
        "insight": "Shows dividend income relative to price.",
    },
    "Payout Ratio": {
        "operator": "<",
        "threshold": 50,
        "unit": "%",
        "insight": "Measures portion of earnings paid as dividends.",
    },
    "Free Cash Flow to Equity": {
        "operator": "custom",
        "unit": "",
        "insight": "Indicates capacity for dividends and buybacks.",
    },
}

SECTION_METRIC_MAP = {
    "Profitability": [
        ("Gross Profit Margin", "gross_profit_margin"),
        ("Operating Margin (EBIT)", "operating_profit_margin"),
        ("Net Profit Margin", "net_profit_margin"),
        ("ROA (Return on Assets)", "return_on_assets"),
        ("ROE (Return on Equity)", "return_on_equity"),
        ("ROIC (Return on Invested Capital)", "return_on_invested_capital"),
    ],
    "Efficiency": [
        ("Asset Turnover", "asset_turnover"),
        ("Inventory Turnover", "inventory_turnover"),
        ("Receivables Turnover", "receivables_turnover"),
        ("Payables Turnover", "payables_turnover"),
        ("Cash Conversion Cycle", "cash_conversion_cycle"),
    ],
    "Liquidity & Solvency": [
        ("Current Ratio", "current_ratio"),
        ("Quick Ratio", "quick_ratio"),
        ("Cash Ratio", "cash_ratio"),
        ("Debt-to-Equity", "debt_to_equity_ratio"),
        ("Debt-to-Assets", "debt_to_assets_ratio"),
        ("Interest Coverage", "interest_coverage_ratio"),
        ("Debt Service Coverage", "debt_service_coverage_ratio"),
    ],
    "Cash Flow Strength": [
        ("Operating Cash Flow / Sales", "operating_cash_flow_sales_ratio"),
        ("Free Cash Flow Margin (FCF/Sales)", "free_cash_flow_margin"),
        ("CapEx / OCF", "capex_to_operating_cash_flow"),
        ("FCF Coverage Ratio", "fcf_coverage_ratio"),
        ("Dividend Payout Ratio", "dividend_payout_ratio"),
    ],
    "Valuation": [
        ("P/E Ratio (Trailing)", "price_to_earnings_ratio"),
        ("P/S Ratio", "price_to_sales_ratio"),
        ("P/B Ratio", "price_to_book_ratio"),
        ("EV/EBITDA", "ev_to_ebitda"),
        ("Earnings Yield", "earnings_yield"),
        ("FCF Yield", "free_cash_flow_yield"),
    ],
    "Growth & Investment": [
        ("R&D / Revenue", "research_and_development_to_revenue"),
        ("CapEx / Revenue", "capex_to_revenue"),
        ("PEG Ratio", "peg_ratio"),
    ],
    "Dividend & Shareholder Returns": [
        ("Dividend Yield", "dividend_yield"),
        ("Payout Ratio", "dividend_payout_ratio"),
        ("Free Cash Flow to Equity", "free_cash_flow_to_equity"),
    ],
}


class FinancialSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = FinancialRepository(session)
        self._company_repository = CompanyRepository(session)

    def upsert_balance_sheets(self, symbol: str, limit: int, period: str):
        """
        Fetch and upsert balance sheets for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted balance sheet records or None if not found
        """
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            balance_sheets_data = self._market_api_client.get_balance_sheets(symbol)
            if not balance_sheets_data:
                logger.info(f"No balance sheet data found for symbol: {symbol}")
                return None

            balance_sheets_in = [
                CompanyBalanceSheetWrite.model_validate(
                    {**bs.model_dump(), "company_id": company.id}
                )
                for bs in balance_sheets_data
            ]
            return self._repository.upsert_balance_sheets(balance_sheets_in)
        except Exception as e:
            logger.error(f"Error upserting balance sheets for {symbol}: {str(e)}")
            raise

    def upsert_income_statements(self, symbol: str, limit: int, period: str):
        """
        Fetch and upsert income statements for a company.
        """
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            income_statements_data = self._market_api_client.get_income_statements(
                symbol
            )
            if not income_statements_data:
                logger.info(f"No income statement data found for symbol: {symbol}")
                return None

            income_statements_in = [
                CompanyIncomeStatementWrite.model_validate(
                    {**is_.model_dump(), "company_id": company.id}
                )
                for is_ in income_statements_data
            ]
            return self._repository.upsert_income_statements(income_statements_in)
        except Exception as e:
            logger.error(f"Error upserting income statements for {symbol}: {str(e)}")
            raise

    def upsert_cash_flow_statements(self, symbol: str, limit: int, period: str):
        """
        Fetch and upsert cash flow statements for a company.
        """
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            cash_flow_statements_data = (
                self._market_api_client.get_cash_flow_statements(symbol)
            )
            if not cash_flow_statements_data:
                logger.info(f"No cash flow statement data found for symbol: {symbol}")
                return None

            cash_flow_statements_in = [
                CompanyCashFlowStatementWrite.model_validate(
                    {**cs.model_dump(), "company_id": company.id}
                )
                for cs in cash_flow_statements_data
            ]
            return self._repository.upsert_cash_flow_statements(cash_flow_statements_in)
        except Exception as e:
            logger.error(f"Error upserting cash flow statements for {symbol}: {str(e)}")
            raise

    def upsert_financial_health(
        self, symbol: str
    ) -> List[CompanyFinancialHealthRead] | None:
        """
        Fetch and upsert financial health data for a company.
        """
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None
            metrics_repo = MetricsRepository(self._repository._db)
            key_metrics_data = metrics_repo.get_financial_ratios_for_year(
                symbol, year="2024"
            )
            financial_ratios_data = metrics_repo.get_financial_ratios_for_year(
                symbol, year="2024"
            )
            print(key_metrics_data.to_dict())
            records = self.map_metrics_to_sections(
                key_metrics=key_metrics_data.to_dict(),
                financial_ratios=financial_ratios_data.to_dict(),
                company_id=company.id,
                symbol=symbol,
            )
            response = self._repository.upsert_financial_health(records)
            return [CompanyFinancialHealthRead.model_validate(fh) for fh in response]

        except Exception as e:
            logger.error(f"Error upserting financial health for {symbol}: {str(e)}")
            raise

    def delete_balance_sheet(self, symbol: str, year: int) -> Optional[Company]:
        return self._repository.delete_balance_sheet(symbol, year)

    def delete_income_statement(self, symbol: str, year: int) -> Optional[Company]:
        return self._repository.delete_income_statement(symbol, year)

    def delete_cash_flow_statement(self, symbol: str, year: int) -> Optional[Company]:
        return self._repository.delete_cash_flow_statement(symbol, year)

    def map_metrics_to_sections(
        self,
        key_metrics: Dict[str, Any],
        financial_ratios: Dict[str, Any],
        company_id: int,
        symbol: str,
    ) -> List[CompanyFinancialHealthWrite]:
        """
        Map raw key_metrics and financial_ratios to sectioned financial health records.
        Compares value to benchmark for status.
        """
        records = []
        data = {**key_metrics, **financial_ratios}
        for section, metrics in SECTION_METRIC_MAP.items():
            for metric_name, key in metrics:
                value = data.get(key)
                benchmark_info = BENCHMARKS_INSIGHTS.get(metric_name)
                insight = benchmark_info["insight"] if benchmark_info else ""
                status = self.compare_value_to_benchmark(value, benchmark_info)
                # Format benchmark for display
                if benchmark_info:
                    if benchmark_info.get("operator") == "range":
                        benchmark = f"{benchmark_info['low']}–{benchmark_info['high']}{benchmark_info['unit']}"
                    elif benchmark_info.get("operator") == "~":
                        benchmark = (
                            f"~{benchmark_info['threshold']}{benchmark_info['unit']}"
                        )
                    elif benchmark_info.get("operator") == "custom":
                        benchmark = "See insight"
                    else:
                        benchmark = f"{benchmark_info['operator']} {benchmark_info['threshold']}{benchmark_info['unit']}"
                else:
                    benchmark = ""
                records.append(
                    CompanyFinancialHealthWrite(
                        company_id=company_id,
                        symbol=symbol,
                        section=section,
                        metric=metric_name,
                        benchmark=benchmark,
                        value=str(value) if value is not None else "",
                        status=status,
                        insight=insight,
                    )
                )
        return records

    def compare_value_to_benchmark(self, value: Any, benchmark: dict) -> str:
        """
        Compare a value to a structured benchmark dict and return status.
        Supports >, <, >=, <=, ~, range, and custom.
        """
        if value is None or benchmark is None:
            return "neutral"
        try:
            # Remove units and symbols for comparison
            value_str = (
                str(value)
                .replace("%", "")
                .replace("×", "")
                .replace("$", "")
                .replace("days", "")
                .replace("B", "")
            )
            value_num = float(re.findall(r"-?\d+\.?\d*", value_str)[0])
        except Exception:
            return "neutral"

        op = benchmark.get("operator")
        benchmark.get("unit", "")
        if op == "range":
            low = benchmark.get("low")
            high = benchmark.get("high")
            if low is not None and high is not None:
                return "healthy" if low <= value_num <= high else "warning"
        elif op == "~":
            threshold = benchmark.get("threshold")
            if threshold is not None:
                return (
                    "healthy"
                    if abs(value_num - threshold) / threshold < 0.15
                    else "warning"
                )
        elif op == ">":
            threshold = benchmark.get("threshold")
            if threshold is not None:
                return "healthy" if value_num > threshold else "warning"
        elif op == "<":
            threshold = benchmark.get("threshold")
            if threshold is not None:
                return "healthy" if value_num < threshold else "warning"
        elif op == ">=":
            threshold = benchmark.get("threshold")
            if threshold is not None:
                return "healthy" if value_num >= threshold else "warning"
        elif op == "<=":
            threshold = benchmark.get("threshold")
            if threshold is not None:
                return "healthy" if value_num <= threshold else "warning"
        elif op == "custom":
            # Always neutral for custom, or implement your own logic
            return "neutral"
        return "neutral"
