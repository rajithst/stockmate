import logging
from sqlalchemy.orm import Session

from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary
from app.schemas.price_target import (
    CompanyPriceTargetSummaryWrite,
    CompanyPriceTargetWrite,
)
from app.repositories.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class CompanyPriceTargetRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_price_targets_by_symbol(self, symbol: str) -> list[CompanyPriceTarget]:
        """Get all price targets for a symbol."""
        return self._get_by_filter(CompanyPriceTarget, {"symbol": symbol})

    def get_price_target_summary_by_symbol(
        self, symbol: str
    ) -> CompanyPriceTargetSummary | None:
        """Get price target summary for a symbol."""
        return self._get_by_filter(
            CompanyPriceTargetSummary, {"symbol": symbol}
        ).first()

    def upsert_price_target(
        self, price_targets: CompanyPriceTargetWrite
    ) -> CompanyPriceTarget:
        """Upsert price target by symbol."""
        return self._upsert_single(
            price_targets,
            CompanyPriceTarget,
            lambda pt: {"symbol": pt.symbol},
            "upsert_price_target",
        )

    def upsert_price_target_summary(
        self, summary_data: CompanyPriceTargetSummaryWrite
    ) -> CompanyPriceTargetSummary:
        """Upsert price target summary by symbol."""
        return self._upsert_single(
            summary_data,
            CompanyPriceTargetSummary,
            lambda s: {"symbol": s.symbol},
            "upsert_price_target_summary",
        )
