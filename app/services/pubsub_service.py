"""
Pub/Sub service for publishing messages to Google Cloud Pub/Sub topics.
"""
import json
import logging
from typing import Any, Optional

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import pubsub_v1

from app.core.config import config

logger = logging.getLogger(__name__)


class PubSubService:
    """Service for publishing company sync messages to Google Cloud Pub/Sub."""

    def __init__(self, project_id: str, credentials_path: Optional[str] = None):
        """
        Initialize the Pub/Sub service.

        Args:
            project_id: Google Cloud project ID
            credentials_path: Path to Google Cloud credentials JSON file (optional)
        """
        self.project_id = project_id
        self.publisher_client = pubsub_v1.PublisherClient()
        self._topics_cache: dict[str, str] = {}

    def _get_topic_path(self, topic_id: str) -> str:
        """Get the full topic path for a given topic ID."""
        if topic_id not in self._topics_cache:
            self._topics_cache[topic_id] = self.publisher_client.topic_path(
                self.project_id, topic_id
            )
        return self._topics_cache[topic_id]

    def publish_message(
        self,
        topic_id: str,
        message_data: dict[str, Any],
        attributes: Optional[dict[str, str]] = None,
    ) -> Optional[str]:
        """
        Publish a message to a Pub/Sub topic.

        Args:
            topic_id: The topic ID to publish to
            message_data: Dictionary containing the message data
            attributes: Optional message attributes for filtering and routing

        Returns:
            Message ID if successful, None otherwise

        Raises:
            GoogleAPICallError: If publishing fails
        """
        try:
            topic_path = self._get_topic_path(topic_id)
            message_json = json.dumps(message_data)
            message_bytes = message_json.encode("utf-8")

            future = self.publisher_client.publish(
                topic_path,
                message_bytes,
                **(attributes or {}),
            )

            message_id = future.result()
            logger.info(
                f"Published message to topic {topic_id}: {message_id}",
                extra={"topic_id": topic_id, "message_id": message_id},
            )
            return message_id

        except GoogleAPICallError as e:
            logger.error(
                f"Failed to publish message to topic {topic_id}: {str(e)}",
                extra={"topic_id": topic_id, "error": str(e)},
            )
            raise

    def publish_company_batch_sync(self, symbols: list[str]) -> Optional[str]:
        """
        Publish a batch of company symbols for sync.

        Args:
            symbols: List of stock symbols to sync

        Returns:
            Message ID if successful, None otherwise
        """
        return self.publish_message(
            topic_id=config.pubsub_company_sync_topic,
            message_data={
                "action": "sync_company_batch",
                "symbols": symbols,
            },
            attributes={"action": "sync_company_batch"},
        )
