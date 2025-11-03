from logging import getLogger
import re
from typing import Any

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.financial_repo import FinancialRepository
from app.repositories.metrics_repo import MetricsRepository
from app.schemas.balance_sheet import CompanyBalanceSheetRead, CompanyBalanceSheetWrite
from app.schemas.cashflow import (
    CompanyCashFlowStatementRead,
    CompanyCashFlowStatementWrite,
)
from app.schemas.financial_health import (
    CompanyFinancialHealthRead,
    CompanyFinancialHealthWrite,
)
from app.schemas.financial_health_config import (
    BENCHMARKS_INSIGHTS,
    SECTION_METRIC_MAP,
)
from app.schemas.income_statement import (
    CompanyIncomeStatementRead,
    CompanyIncomeStatementWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = getLogger(__name__)


class FinancialSyncService(BaseSyncService):
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        super().__init__(market_api_client, session)
        self._repository = FinancialRepository(session)
        self._metrics_repository = MetricsRepository(session)

    def upsert_balance_sheets(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyBalanceSheetRead] | None:
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
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            api_data = self._market_api_client.get_balance_sheets(
                symbol, period=period, limit=limit
            )
            if not self._validate_api_response(api_data, "balance_sheets", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyBalanceSheetWrite
            )
            persisted_records = self._repository.upsert_balance_sheets(
                records_to_persist
            )
            result = self._map_schema_list(persisted_records, CompanyBalanceSheetRead)

            self._log_sync_success("balance_sheets", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("balance_sheets", symbol, e)
            raise

    def upsert_income_statements(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyIncomeStatementRead] | None:
        """
        Fetch and upsert income statements for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted income statement records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            api_data = self._market_api_client.get_income_statements(
                symbol, period=period, limit=limit
            )
            if not self._validate_api_response(api_data, "income_statements", symbol):
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyIncomeStatementWrite
            )
            persisted_records = self._repository.upsert_income_statements(
                records_to_persist
            )
            result = self._map_schema_list(
                persisted_records, CompanyIncomeStatementRead
            )

            self._log_sync_success("income_statements", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("income_statements", symbol, e)
            raise

    def upsert_cash_flow_statements(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyCashFlowStatementRead] | None:
        """
        Fetch and upsert cash flow statements for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted cash flow statement records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            api_data = self._market_api_client.get_cash_flow_statements(
                symbol, period=period, limit=limit
            )
            if not self._validate_api_response(
                api_data, "cash_flow_statements", symbol
            ):
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyCashFlowStatementWrite
            )
            persisted_records = self._repository.upsert_cash_flow_statements(
                records_to_persist
            )
            result = self._map_schema_list(
                persisted_records, CompanyCashFlowStatementRead
            )

            self._log_sync_success("cash_flow_statements", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("cash_flow_statements", symbol, e)
            raise

    def upsert_financial_health(
        self, symbol: str
    ) -> list[CompanyFinancialHealthRead] | None:
        """
        Fetch and upsert financial health data for a company.

        Combines latest key metrics and financial ratios to generate financial
        health scores across multiple sections (profitability, efficiency, etc).

        Args:
            symbol: Stock symbol

        Returns:
            List of financial health records or None if not found
        """
        try:
            # Get company or return None
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Get latest metrics data
            key_metrics_data = self._metrics_repository.get_latest_key_metrics(symbol)
            financial_ratios_data = (
                self._metrics_repository.get_latest_financial_ratios(symbol)
            )

            if not key_metrics_data or not financial_ratios_data:
                logger.info(
                    f"No metrics data found for financial health analysis: {symbol}"
                )
                return None

            # Map metrics to sections
            records = self.map_metrics_to_sections(
                key_metrics=key_metrics_data.to_dict(),
                financial_ratios=financial_ratios_data.to_dict(),
                company_id=company.id,
                symbol=symbol,
            )

            # Persist and return
            response = self._repository.upsert_financial_health(records)
            result = self._map_schema_list(response, CompanyFinancialHealthRead)

            self._log_sync_success("financial_health", len(result), symbol)
            return result

        except Exception as e:
            self._log_sync_failure("financial_health", symbol, e)
            raise

    def delete_balance_sheet(self, symbol: str, year: int) -> bool:
        """Delete a balance sheet by symbol and year."""
        return self._repository.delete_balance_sheet(symbol, year)

    def delete_income_statement(self, symbol: str, year: int) -> bool:
        """Delete an income statement by symbol and year."""
        return self._repository.delete_income_statement(symbol, year)

    def delete_cash_flow_statement(self, symbol: str, year: int) -> bool:
        """Delete a cash flow statement by symbol and year."""
        return self._repository.delete_cash_flow_statement(symbol, year)

    def map_metrics_to_sections(
        self,
        key_metrics: dict[str, Any],
        financial_ratios: dict[str, Any],
        company_id: int,
        symbol: str,
    ) -> list[CompanyFinancialHealthWrite]:
        """
        Map raw key_metrics and financial_ratios to sectioned financial health records.

        Compares each value to its benchmark and generates status (healthy/warning/neutral).

        Args:
            key_metrics: Dictionary of key metrics data
            financial_ratios: Dictionary of financial ratios data
            company_id: Company ID to associate with records
            symbol: Stock symbol

        Returns:
            List of financial health write records
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
