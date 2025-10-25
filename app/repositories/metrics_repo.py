from sqlalchemy.orm import Session

from app.db.models.financial_ratio import CompanyFinancialRatio
from app.db.models.financial_score import CompanyFinancialScore
from app.db.models.key_metrics import CompanyKeyMetrics
from app.schemas.financial_ratio import CompanyFinancialRatioWrite
from app.schemas.financial_score import CompanyFinancialScoresWrite
from app.schemas.key_metrics import CompanyKeyMetricsWrite
from app.util.model_mapper import map_model


class MetricsRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_key_metrics_by_symbol(self, symbol: str) -> list[CompanyKeyMetrics]:
        return (
            self._db.query(CompanyKeyMetrics)
            .filter(CompanyKeyMetrics.symbol == symbol)
            .all()
        )

    def get_financial_ratios_by_symbol(
        self, symbol: str
    ) -> list[CompanyFinancialRatio]:
        return (
            self._db.query(CompanyFinancialRatio)
            .filter(CompanyFinancialRatio.symbol == symbol)
            .all()
        )

    def get_financial_scores_by_symbol(
        self, symbol: str
    ) -> list[CompanyFinancialScore]:
        return (
            self._db.query(CompanyFinancialScore)
            .filter(CompanyFinancialScore.symbol == symbol)
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

    def upsert_financial_ratios(
        self, financial_ratios: list[CompanyFinancialRatioWrite]
    ) -> list[CompanyFinancialRatio] | None:
        records = []
        for ratio in financial_ratios:
            existing = (
                self._db.query(CompanyFinancialRatio)
                .filter_by(symbol=ratio.symbol, date=ratio.date)
                .first()
            )
            if existing:
                record = map_model(existing, ratio)
            else:
                record = CompanyFinancialRatio(**ratio.model_dump(exclude_unset=True))
                self._db.add(record)
            records.append(record)
        self._db.commit()
        for record in records:
            self._db.refresh(record)
        return records

    def upsert_financial_scores(
        self, financial_scores: CompanyFinancialScoresWrite
    ) -> CompanyFinancialScore | None:
        existing = (
            self._db.query(CompanyFinancialScore)
            .filter_by(symbol=financial_scores.symbol)
            .first()
        )
        if existing:
            record = map_model(existing, financial_scores)
        else:
            record = CompanyFinancialScore(
                **financial_scores.model_dump(exclude_unset=True)
            )
            self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record
