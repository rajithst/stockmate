import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.company_metrics import (
    CompanyAnalystEstimate,
    CompanyDiscountedCashFlow,
    CompanyKeyMetrics,
    CompanyRevenueProductSegmentation,
)
from app.schemas.company_metrics import (
    CompanyAnalystEstimateWrite,
    CompanyDiscountedCashFlowWrite,
    CompanyKeyMetricsWrite,
    CompanyRevenueProductSegmentationWrite,
)
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class CompanyMetricsSyncRepository:
    """Repository for multiple company metrics entities (analyst estimates, key metrics, DCF, revenue segmentation)."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def upsert_analyst_estimates(
        self, estimates: list[CompanyAnalystEstimateWrite]
    ) -> list[CompanyAnalystEstimate]:
        """Bulk upsert analyst estimates by company_id and date."""
        try:
            results = []
            for estimate_in in estimates:
                # Find existing record
                existing = (
                    self._db.query(CompanyAnalystEstimate)
                    .filter_by(company_id=estimate_in.company_id, date=estimate_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, estimate_in)
                else:
                    # Create new
                    result = CompanyAnalystEstimate(
                        **estimate_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} analyst estimates")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_analyst_estimates: {e}")
            raise

    def upsert_key_metrics(
        self, key_metrics: list[CompanyKeyMetricsWrite]
    ) -> list[CompanyKeyMetrics]:
        """Bulk upsert key metrics by symbol and date."""
        try:
            results = []
            for metric_in in key_metrics:
                # Find existing record
                existing = (
                    self._db.query(CompanyKeyMetrics)
                    .filter_by(symbol=metric_in.symbol, date=metric_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, metric_in)
                else:
                    # Create new
                    result = CompanyKeyMetrics(
                        **metric_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} key metrics")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_key_metrics: {e}")
            raise

    def upsert_discounted_cash_flow(
        self, dcf_in: CompanyDiscountedCashFlowWrite
    ) -> CompanyDiscountedCashFlow:
        """Upsert DCF record by company_id."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyDiscountedCashFlow)
                .filter_by(company_id=dcf_in.company_id)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, dcf_in)
            else:
                # Create new
                result = CompanyDiscountedCashFlow(
                    **dcf_in.model_dump(exclude_unset=True)
                )
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(f"Upserted DCF record for company_id {dcf_in.company_id}")
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_discounted_cash_flow: {e}")
            raise

    def upsert_revenue_segmentations(
        self,
        segmentations_in: list[CompanyRevenueProductSegmentationWrite],
    ) -> list[CompanyRevenueProductSegmentation]:
        """Bulk upsert revenue product segmentation records by symbol, date, and period."""
        try:
            results = []
            for segmentation_in in segmentations_in:
                # Find existing record
                existing = (
                    self._db.query(CompanyRevenueProductSegmentation)
                    .filter_by(
                        symbol=segmentation_in.symbol,
                        date=segmentation_in.date,
                        period=segmentation_in.period,
                    )
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, segmentation_in)
                else:
                    # Create new
                    result = CompanyRevenueProductSegmentation(
                        **segmentation_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} revenue segmentations")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_revenue_segmentations: {e}")
            raise
