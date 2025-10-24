from sqlalchemy.orm import Session

from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary
from app.schemas.price_target import CompanyPriceTargetWrite
from app.util import model_mapper


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

    def upsert_price_targets(
        self, price_targets: list[CompanyPriceTargetWrite]
    ) -> list[CompanyPriceTarget] | None:
        records = []
        for price_target in price_targets:
            existing = (
                self._db.query(CompanyPriceTarget)
                .filter_by(symbol=price_target.symbol, date=price_target.date)
                .first()
            )
            if existing:
                record = model_mapper(existing, price_target)
            else:
                record = CompanyPriceTarget(
                    **price_target.model_dump(exclude_unset=True)
                )
                self._db.add(record)
            records.append(record)
        self._db.commit()
        for record in records:
            self._db.refresh(record)
        return records

    def upsert_price_target_summary(
        self, summary_data: CompanyPriceTargetWrite
    ) -> CompanyPriceTargetSummary:
        existing = (
            self._db.query(CompanyPriceTargetSummary)
            .filter_by(symbol=summary_data.symbol)
            .first()
        )

        if existing:
            summary = model_mapper(existing, summary_data)
        else:
            summary = CompanyPriceTargetSummary(
                **summary_data.model_dump(exclude_unset=True)
            )
            self._db.add(summary)

        self._db.commit()
        self._db.refresh(summary)

        return summary
