from sqlalchemy.orm import Session

from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary
from app.schemas.price_target import (
    CompanyPriceTargetSummaryWrite,
    CompanyPriceTargetWrite,
)
from app.util.model_mapper import map_model


class CompanyPriceTargetRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_price_targets_by_symbol(self, symbol: str) -> list[CompanyPriceTarget]:
        return (
            self._db.query(CompanyPriceTarget)
            .filter(CompanyPriceTarget.symbol == symbol)
            .all()
        )

    def get_price_target_summary_by_symbol(
        self, symbol: str
    ) -> CompanyPriceTargetSummary | None:
        return (
            self._db.query(CompanyPriceTargetSummary)
            .filter(CompanyPriceTargetSummary.symbol == symbol)
            .first()
        )

    def upsert_price_target(
        self, price_targets: CompanyPriceTargetWrite
    ) -> CompanyPriceTarget | None:
        existing = (
            self._db.query(CompanyPriceTarget)
            .filter_by(symbol=price_targets.symbol)
            .first()
        )
        if existing:
            record = map_model(existing, price_targets)
        else:
            record = CompanyPriceTarget(**price_targets.model_dump(exclude_unset=True))
            self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record

    def upsert_price_target_summary(
        self, summary_data: CompanyPriceTargetSummaryWrite
    ) -> CompanyPriceTargetSummary:
        existing = (
            self._db.query(CompanyPriceTargetSummary)
            .filter_by(symbol=summary_data.symbol)
            .first()
        )

        if existing:
            summary = map_model(existing, summary_data)
        else:
            summary = CompanyPriceTargetSummary(
                **summary_data.model_dump(exclude_unset=True)
            )
            self._db.add(summary)

        self._db.commit()
        self._db.refresh(summary)

        return summary
