from logging import getLogger
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.grading_repo import GradingRepository, GradingSummaryRepository
from app.schemas.grading import (
    CompanyGradingRead,
    CompanyGradingSummaryRead,
    CompanyGradingSummaryWrite,
    CompanyGradingWrite,
)

logger = getLogger(__name__)


class GradingSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._grading_repository = GradingRepository(session)
        self._grading_summary_repository = GradingSummaryRepository(session)
        self._company_repository = CompanyRepository(session)

    def get_gradings(self, symbol: str, limit: int = 10) -> list[CompanyGradingRead]:
        gradings = self._grading_repository.get_gradings_by_symbol(symbol, limit)
        return [
            CompanyGradingRead.model_validate(grading.model_dump())
            for grading in gradings
        ]

    def upsert_gradings(self, symbol: str) -> list[CompanyGradingRead] | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(
                    f"Company with symbol {symbol} not found in the database."
                )
                return None

            grading_data = self._market_api_client.get_company_gradings(symbol)
            if not grading_data:
                logger.info(
                    f"No grading data found for symbol {symbol} from external API."
                )
                return None
            grading_in = [
                CompanyGradingWrite.model_validate(
                    {
                        **grading.model_dump(),
                        "company_id": company.id,
                    }
                )
                for grading in grading_data
            ]
            gradings = self._grading_repository.upsert_grading(symbol, grading_in)
            return [CompanyGradingRead.model_validate(grading) for grading in gradings]
        except Exception as e:
            logger.error(f"Error upserting gradings for symbol {symbol}: {e}")
            return None

    def upsert_grading_summary(self, symbol: str) -> CompanyGradingRead | None:
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(
                    f"Company with symbol {symbol} not found in the database."
                )
                return None

            summary_data = self._market_api_client.get_company_grading_summary(symbol)
            if not summary_data:
                logger.info(
                    f"No grading summary data found for symbol {symbol} from external API."
                )
                return None
            summary_in = CompanyGradingSummaryWrite.model_validate(
                {**summary_data.model_dump(), "company_id": company.id}
            )
            summary = self._grading_summary_repository.upsert_grading_summary(
                summary_in
            )
            return CompanyGradingSummaryRead.model_validate(summary)
        except Exception as e:
            logger.error(f"Error upserting grading summary for symbol {symbol}: {e}")
            return None
