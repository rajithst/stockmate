from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
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

logger = getLogger(__name__)


class MetricsSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = MetricsRepository(session)
        self._company_repository = CompanyRepository(session)

    def get_key_metrics(self, symbol: str) -> list[CompanyKeyMetricsRead]:
        key_metrics = self._repository.get_key_metrics_by_symbol(symbol)
        return [CompanyKeyMetricsRead.model_validate(km) for km in key_metrics]

    def get_financial_ratios(self, symbol: str) -> list[CompanyFinancialRatioRead]:
        financial_ratios = self._repository.get_financial_ratios_by_symbol(symbol)
        return [CompanyFinancialRatioRead.model_validate(fr) for fr in financial_ratios]

    def get_financial_scores(self, symbol: str) -> list[CompanyFinancialScoresRead]:
        financial_scores = self._repository.get_financial_scores_by_symbol(symbol)
        return [
            CompanyFinancialScoresRead.model_validate(fs) for fs in financial_scores
        ]

    def upsert_key_metrics(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyKeyMetricsRead] | None:
        """
        Fetch and upsert key metrics for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted key metrics records or None if not found
        """
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_snapshot_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            key_metrics_data = self._market_api_client.get_key_metrics(
                symbol, period, limit
            )
            if not key_metrics_data:
                logger.info(f"No key metrics data found for symbol: {symbol}")
                return None

            key_metrics_in = [
                CompanyKeyMetricsWrite.model_validate(
                    {**km.model_dump(), "company_id": company.id}
                )
                for km in key_metrics_data
            ]
            key_metrics = self._repository.upsert_key_metrics(key_metrics_in)
            return [CompanyKeyMetricsRead.model_validate(km) for km in key_metrics]
        except Exception as e:
            logger.error(f"Error upserting key metrics for {symbol}: {str(e)}")
            raise

    def upsert_financial_ratios(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyFinancialRatioRead] | None:
        """
        Fetch and upsert financial ratios for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted financial ratio records or None if not found
        """
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_snapshot_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            financial_ratios_data = self._market_api_client.get_financial_ratios(
                symbol, period, limit
            )
            if not financial_ratios_data:
                logger.info(f"No financial ratios data found for symbol: {symbol}")
                return None

            financial_ratios_in = [
                CompanyFinancialRatioWrite.model_validate(
                    {**fr.model_dump(), "company_id": company.id}
                )
                for fr in financial_ratios_data
            ]
            financial_ratios = self._repository.upsert_financial_ratios(
                financial_ratios_in
            )
            return [
                CompanyFinancialRatioRead.model_validate(fr) for fr in financial_ratios
            ]
        except Exception as e:
            logger.error(f"Error upserting financial ratios for {symbol}: {str(e)}")
            raise

    def upsert_financial_scores(self, symbol: str) -> CompanyFinancialScoresRead | None:
        """
        Fetch and upsert financial scores for a company.

        Args:
            symbol: Stock symbol

        Returns:
            Upserted financial scores record or None if not found
        """
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_snapshot_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            financial_scores_data = self._market_api_client.get_financial_scores(symbol)
            if not financial_scores_data:
                logger.info(f"No financial scores data found for symbol: {symbol}")
                return None

            financial_scores_in = CompanyFinancialScoresWrite.model_validate(
                {**financial_scores_data.model_dump(), "company_id": company.id}
            )
            financial_scores = self._repository.upsert_financial_scores(
                financial_scores_in
            )
            return CompanyFinancialScoresRead.model_validate(financial_scores)
        except Exception as e:
            logger.error(f"Error upserting financial scores for {symbol}: {str(e)}")
            raise
