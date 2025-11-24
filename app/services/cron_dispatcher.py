"""
Cron dispatcher for scheduling and publishing company batch sync messages to Pub/Sub.
"""
import logging
from datetime import datetime

from app.repositories.company_repo import CompanyRepository
from app.services.pubsub_service import PubSubService

logger = logging.getLogger(__name__)


class CronDispatcher:
    """Dispatcher for scheduling company batch syncs via Pub/Sub."""

    def __init__(self, pubsub_service: PubSubService, company_repo: CompanyRepository):
        """
        Initialize the cron dispatcher.

        Args:
            pubsub_service: PubSubService instance for publishing messages
            company_repo: CompanyRepository instance for fetching all companies
        """
        self.pubsub_service = pubsub_service
        self.company_repo = company_repo

    def dispatch_weekly_company_sync(self, batch_size: int = 10) -> dict:
        """
        Dispatch batch company sync jobs to Pub/Sub.
        Fetches all companies from DB and publishes them in batches.

        Args:
            batch_size: Number of companies per batch message

        Returns:
            Dictionary with dispatch results and statistics
        """
        logger.info(
            "Starting weekly company sync dispatch",
            extra={"timestamp": datetime.utcnow()},
        )

        try:
            # Fetch all companies from database
            companies = self.company_repo.get_all_companies()
            symbols = [company.symbol for company in companies]

            if not symbols:
                logger.warning("No companies found in database to sync")
                return {
                    "status": "no_companies",
                    "total_companies": 0,
                    "total_batches": 0,
                    "message_ids": [],
                }

            # Create batches and publish
            batches = [symbols[i : i + batch_size] for i in range(0, len(symbols), batch_size)]
            message_ids = []

            logger.info(
                f"Dispatching {len(symbols)} companies in {len(batches)} batches",
                extra={"total_companies": len(symbols), "batch_count": len(batches)},
            )

            for batch_idx, batch in enumerate(batches):
                try:
                    message_id = self.pubsub_service.publish_company_batch_sync(batch)
                    message_ids.append(message_id)
                    logger.info(
                        f"Published batch {batch_idx + 1}/{len(batches)}",
                        extra={"batch_size": len(batch), "message_id": message_id},
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to publish batch {batch_idx + 1}: {str(e)}",
                        extra={"batch_idx": batch_idx, "error": str(e)},
                    )
                    # Continue with next batch even if one fails
                    message_ids.append(None)

            successful_batches = sum(1 for mid in message_ids if mid is not None)

            return {
                "status": "success" if successful_batches == len(batches) else "partial",
                "total_companies": len(symbols),
                "total_batches": len(batches),
                "successful_batches": successful_batches,
                "failed_batches": len(batches) - successful_batches,
                "message_ids": message_ids,
            }

        except Exception as e:
            logger.error(
                f"Failed to dispatch company sync: {str(e)}",
                extra={"error": str(e)},
                exc_info=True,
            )
            return {
                "status": "error",
                "error": str(e),
            }
