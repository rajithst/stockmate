from sqlalchemy.orm import Session

from app.db.models.grading import CompanyGrading, CompanyGradingSummary
from app.schemas.grading import CompanyGradingSummaryWrite, CompanyGradingWrite
from app.util.map_model import map_model


class GradingRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_gradings_by_symbol(
        self, symbol: str, limit: int = 100
    ) -> list[CompanyGrading]:
        return (
            self._db.query(CompanyGrading)
            .filter(CompanyGrading.company_symbol == symbol)
            .order_by(CompanyGrading.date.desc())
            .limit(limit)
            .all()
        )

    def upsert_grading(
        self, symbol: str, grading_data: list[CompanyGradingWrite]
    ) -> list[CompanyGrading] | None:
        grading_records = []
        for grading in grading_data:
            existing = (
                self._db.query(CompanyGrading)
                .filter_by(company_symbol=symbol, date=grading.date)
                .first()
            )
            if existing:
                grading_record = map_model(existing, grading)
            else:
                grading_record = CompanyGrading(
                    **grading.model_dump(exclude_unset=True)
                )
                self._db.add(grading_record)
            grading_records.append(grading_record)
        self._db.commit()
        for record in grading_records:
            self._db.refresh(record)
        return grading_records


class GradingSummaryRepository:
    def __init__(self, session: Session):
        self._db = session

    def upsert_grading_summary(
        self, summary_data: CompanyGradingSummaryWrite
    ) -> CompanyGradingSummary:
        existing = (
            self._db.query(CompanyGradingSummary)
            .filter_by(company_symbol=summary_data.symbol)
            .first()
        )

        if existing:
            summary = map_model(existing, summary_data)
        else:
            summary = CompanyGradingSummary(
                **summary_data.model_dump(exclude_unset=True)
            )
            self._db.add(summary)
        self._db.commit()
        self._db.refresh(summary)
        return summary
