from sqlalchemy.orm import Session

from app.db.models.financial_ratio import CompanyFinancialRatio
from app.db.models.financial_score import CompanyFinancialScore
from app.db.models.key_metrics import CompanyKeyMetrics
from app.schemas.financial_ratio import CompanyFinancialRatioWrite
from app.schemas.financial_score import CompanyFinancialScoresWrite
from app.schemas.key_metrics import CompanyKeyMetricsWrite
from app.repositories.base_repo import BaseRepository


class MetricsRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_key_metrics_by_symbol(self, symbol: str) -> list[CompanyKeyMetrics]:
        return self._get_by_filter(CompanyKeyMetrics, {"symbol": symbol})

    def get_financial_ratios_by_symbol(
        self, symbol: str
    ) -> list[CompanyFinancialRatio]:
        return self._get_by_filter(CompanyFinancialRatio, {"symbol": symbol})

    def get_financial_scores_by_symbol(
        self, symbol: str
    ) -> list[CompanyFinancialScore]:
        return self._get_by_filter(CompanyFinancialScore, {"symbol": symbol})

    def get_latest_key_metrics(self, symbol: str) -> CompanyKeyMetrics | None:
        """Get the latest key metrics."""
        metrics = self._get_by_filter(
            CompanyKeyMetrics,
            {"symbol": symbol},
            order_by_desc=CompanyKeyMetrics.fiscal_year,
            limit=1,
        )
        if metrics:
            return metrics[0]
        return None

    def get_latest_financial_ratios(self, symbol: str) -> CompanyFinancialRatio | None:
        """Get the latest financial ratios."""
        metrics = self._get_by_filter(
            CompanyFinancialRatio,
            {"symbol": symbol},
            order_by_desc=CompanyFinancialRatio.fiscal_year,
            limit=1,
        )
        if metrics:
            return metrics[0]
        return None

    def upsert_key_metrics(
        self, key_metrics: list[CompanyKeyMetricsWrite]
    ) -> list[CompanyKeyMetrics]:
        """Upsert key metrics using the base class pattern."""
        return self._upsert_records(
            key_metrics,
            CompanyKeyMetrics,
            lambda km: {"symbol": km.symbol, "date": km.date},
            "upsert_key_metrics",
        )

    def upsert_financial_ratios(
        self, financial_ratios: list[CompanyFinancialRatioWrite]
    ) -> list[CompanyFinancialRatio]:
        """Upsert financial ratios using the base class pattern."""
        return self._upsert_records(
            financial_ratios,
            CompanyFinancialRatio,
            lambda fr: {"symbol": fr.symbol, "date": fr.date},
            "upsert_financial_ratios",
        )

    def upsert_financial_scores(
        self, financial_scores: CompanyFinancialScoresWrite
    ) -> CompanyFinancialScore | None:
        return self._upsert_single(
            financial_scores,
            CompanyFinancialScore,
            lambda fs: {"symbol": financial_scores.symbol},
            "upsert_financial_scores",
        )
