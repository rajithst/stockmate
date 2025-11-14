import logging
import re
from typing import Any

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.internal.financial_health_sync_repo import (
    CompanyFinancialHealthSyncRepository,
)
from app.schemas.financial_health import (
    CompanyFinancialHealthRead,
    CompanyFinancialHealthWrite,
    CompanyFinancialScoresRead,
    CompanyFinancialScoresWrite,
)
from app.schemas.financial_health_config import BENCHMARKS_INSIGHTS, SECTION_METRIC_MAP
from app.services.internal.base_sync_service import BaseSyncService

logger = logging.getLogger(__name__)


class CompanyFinancialHealthSyncService(BaseSyncService):
    """Service for syncing company financial health data from FMP API."""

    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        super().__init__(session)
        self._market_api_client = market_api_client
        self._repository = CompanyFinancialHealthSyncRepository(session)

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
            records = self._map_metrics_to_sections(
                key_metrics=key_metrics_data.to_dict(),
                financial_ratios=financial_ratios_data.to_dict(),
                company_id=company.id,
                symbol=symbol,
            )

            # Persist and return
            response = self._repository.upsert_financial_health(records)
            result = self._map_schema_list(response, CompanyFinancialHealthRead)

            logger.info(
                f"Upserted financial health for {symbol}, records: {len(result)}"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to upsert financial health for {symbol}: {e}")
            raise

    def _map_metrics_to_sections(
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
                status = self._compare_value_to_benchmark(value, benchmark_info)

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

    def _compare_value_to_benchmark(self, value: Any, benchmark: dict) -> str:
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

    def upsert_financial_scores(self, symbol: str) -> CompanyFinancialScoresRead | None:
        """
        Fetch and upsert financial scores for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted financial scores record or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            financial_scores_data = self._market_api_client.get_financial_scores(symbol)
            if not financial_scores_data:
                logger.error(f"No data returned for financial scores of {symbol}")
                return None

            financial_scores_in = self._add_company_id_to_record(
                financial_scores_data, company.id, CompanyFinancialScoresWrite
            )
            financial_scores = self._repository.upsert_financial_scores(
                financial_scores_in
            )
            result = self._map_schema_single(
                financial_scores, CompanyFinancialScoresRead
            )

            logger.info(f"Successfully synced financial scores for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync financial scores for {symbol}: {str(e)}", exc_info=True
            )
            raise
