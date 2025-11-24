"""
Pub/Sub message handler for processing incoming company batch sync messages.
"""
import base64
import json
import logging
from typing import Any

from app.services.internal.company_sync_service import CompanySyncService

logger = logging.getLogger(__name__)


class PubSubHandler:
    """Handler for processing Pub/Sub company sync messages."""

    def __init__(self, company_sync_service: CompanySyncService):
        """
        Initialize the Pub/Sub handler.

        Args:
            company_sync_service: Service for syncing company data
        """
        self.company_sync_service = company_sync_service

    def decode_pubsub_message(self, message: dict[str, Any]) -> dict[str, Any]:
        """
        Decode a Pub/Sub message from the push subscription format.

        Args:
            message: The message dict from Pub/Sub push subscription

        Returns:
            Decoded message data

        Raises:
            ValueError: If the message format is invalid
        """
        try:
            if "message" not in message:
                raise ValueError("Invalid Pub/Sub message: missing 'message' field")

            message_data = message.get("message", {})
            if "data" not in message_data:
                raise ValueError("Invalid Pub/Sub message: missing 'data' field")

            encoded_data = message_data.get("data")
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
            message_payload = json.loads(decoded_data)

            logger.info(
                "Decoded Pub/Sub message",
                extra={
                    "message_id": message_data.get("messageId"),
                    "payload": message_payload,
                },
            )
            return message_payload

        except (ValueError, KeyError, json.JSONDecodeError) as e:
            logger.error(
                f"Failed to decode Pub/Sub message: {str(e)}", extra={"error": str(e)}
            )
            raise

    async def handle_message(self, message: dict[str, Any]) -> dict[str, Any]:
        """
        Handle an incoming Pub/Sub message.

        Args:
            message: The decoded message payload

        Returns:
            Result of the message processing

        Raises:
            ValueError: If the action is not recognized
        """
        action = message.get("action")

        if action == "sync_company_batch":
            return await self._handle_sync_company_batch(message)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def _handle_sync_company_batch(
        self, message: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Handle a batch company sync message.

        Args:
            message: The message payload with symbols list

        Returns:
            Result dictionary
        """
        symbols = message.get("symbols", [])

        if not symbols:
            raise ValueError("Missing 'symbols' in message")

        logger.info(
            f"Starting batch company sync for {len(symbols)} companies",
            extra={"symbols": symbols},
        )

        try:
            results = {}
            success_count = 0
            failed_count = 0

            for symbol in symbols:
                try:
                    self.company_sync_service.upsert_company(symbol)
                    results[symbol] = "success"
                    success_count += 1
                    logger.info(f"Successfully synced {symbol}")
                except Exception as e:
                    results[symbol] = f"error: {str(e)}"
                    failed_count += 1
                    logger.error(f"Failed to sync {symbol}: {str(e)}")

            return {
                "status": "completed",
                "action": "sync_company_batch",
                "total": len(symbols),
                "success": success_count,
                "failed": failed_count,
                "results": results,
            }

        except Exception as e:
            logger.error(
                f"Failed batch company sync: {str(e)}",
                extra={"error": str(e)},
                exc_info=True,
            )
            return {
                "status": "error",
                "action": "sync_company_batch",
                "error": str(e),
            }
