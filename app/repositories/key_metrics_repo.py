from sqlalchemy.orm import Session

from app.db.models.key_metrics import CompanyKeyMetrics
from app.schemas.key_metrics import CompanyKeyMetricsWrite
from app.util import map_model


class KeyMetricsRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_key_metrics_by_symbol(self, symbol: str) -> list[CompanyKeyMetrics]:
        return (
            self._db.query(CompanyKeyMetrics)
            .filter(CompanyKeyMetrics.symbol == symbol)
            .all()
        )

    def upsert_key_metrics(
        self, key_metrics: list[CompanyKeyMetricsWrite]
    ) -> list[CompanyKeyMetrics] | None:
        records = []
        for key_metric in key_metrics:
            existing = (
                self._db.query(CompanyKeyMetrics)
                .filter_by(symbol=key_metric.symbol, date=key_metric.date)
                .first()
            )
            if existing:
                record = map_model(existing, key_metric)
            else:
                record = CompanyKeyMetrics(**key_metric.model_dump(exclude_unset=True))
                self._db.add(record)
            records.append(record)
        self._db.commit()
        for record in records:
            self._db.refresh(record)
        return records
