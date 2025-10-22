from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.metrics_repo import MetricsRepository
from app.schemas.financial_ratio import (
    CompanyFinancialRatioRead,
    CompanyFinancialRatioWrite,
)
from app.schemas.financial_score import (
    CompanyFinancialScoresRead,
    CompanyFinancialScoresWrite,
)
from app.schemas.key_metrics import CompanyKeyMetricsRead, CompanyKeyMetricsWrite


class MetricsSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = MetricsRepository(session)

    def get_key_metrics(self, symbol: str) -> list[CompanyKeyMetricsRead]:
        key_metrics = self._repository.get_key_metrics_by_symbol(symbol)
        return [
            CompanyKeyMetricsRead.model_validate(km.model_dump()) for km in key_metrics
        ]

    def get_financial_ratios(self, symbol: str) -> list[CompanyFinancialRatioRead]:
        financial_ratios = self._repository.get_financial_ratios_by_symbol(symbol)
        return [
            CompanyFinancialRatioRead.model_validate(fr.model_dump())
            for fr in financial_ratios
        ]

    def get_financial_scores(self, symbol: str) -> list[CompanyFinancialScoresRead]:
        financial_scores = self._repository.get_financial_scores_by_symbol(symbol)
        return [
            CompanyFinancialScoresRead.model_validate(fs.model_dump())
            for fs in financial_scores
        ]

    def upsert_key_metrics(
        self, symbol: str, limit: int, period: str
    ) -> list[CompanyKeyMetricsRead] | None:
        key_metrics_data = self._market_api_client.get_company_key_metrics(
            symbol, limit, period
        )
        if not key_metrics_data:
            return None
        key_metrics_in = [
            CompanyKeyMetricsWrite.model_validate(km.model_dump())
            for km in key_metrics_data
        ]
        key_metrics = self._repository.upsert_key_metrics(key_metrics_in)
        return [
            CompanyKeyMetricsRead.model_validate(km.model_dump()) for km in key_metrics
        ]

    def upsert_financial_ratios(
        self, symbol: str, limit: int, period: str
    ) -> list[CompanyFinancialRatioRead] | None:
        financial_ratios_data = self._market_api_client.get_company_financial_ratios(
            symbol, limit, period
        )
        if not financial_ratios_data:
            return None
        financial_ratios_in = [
            CompanyFinancialRatioWrite.model_validate(fr.model_dump())
            for fr in financial_ratios_data
        ]
        financial_ratios = self._repository.upsert_financial_ratios(financial_ratios_in)
        return [
            CompanyFinancialRatioRead.model_validate(fr.model_dump())
            for fr in financial_ratios
        ]

    def upsert_financial_scores(self, symbol: str) -> CompanyFinancialScoresRead | None:
        financial_scores_data = self._market_api_client.get_company_financial_scores(
            symbol
        )
        if not financial_scores_data:
            return None
        financial_scores_in = CompanyFinancialScoresWrite.model_validate(
            financial_scores_data.model_dump()
        )
        financial_scores = self._repository.upsert_financial_scores(financial_scores_in)
        return CompanyFinancialScoresRead.model_validate(financial_scores.model_dump())
