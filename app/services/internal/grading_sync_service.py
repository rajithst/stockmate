from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.grading_repo import GradingRepository, GradingSummaryRepository
from app.schemas.grading import (
    CompanyGradingRead,
    CompanyGradingSummaryRead,
    CompanyGradingSummaryWrite,
    CompanyGradingWrite,
)


class GradingSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._grading_repository = GradingRepository(session)
        self._grading_summary_repository = GradingSummaryRepository(session)

    def get_gradings(self, symbol: str, limit: int = 10) -> list[CompanyGradingRead]:
        gradings = self._grading_repository.get_gradings_by_symbol(symbol, limit)
        return [
            CompanyGradingRead.model_validate(grading.model_dump())
            for grading in gradings
        ]

    def upsert_gradings(self, symbol: str) -> list[CompanyGradingRead] | None:
        grading_data = self._market_api_client.get_company_gradings(symbol)
        if not grading_data:
            return None
        grading_in = [
            CompanyGradingWrite.model_validate(grading.model_dump())
            for grading in grading_data
        ]
        gradings = self._grading_repository.upsert_grading(symbol, grading_in)
        return [
            CompanyGradingRead.model_validate(grading.model_dump())
            for grading in gradings
        ]

    def upsert_grading_summary(self, symbol: str) -> CompanyGradingRead | None:
        summary_data = self._market_api_client.get_company_grading_summary(symbol)
        if not summary_data:
            return None
        summary_in = CompanyGradingSummaryWrite.model_validate(
            summary_data.model_dump()
        )
        summary = self._grading_summary_repository.upsert_grading_summary(summary_in)
        return CompanyGradingSummaryRead.model_validate(summary.model_dump())
