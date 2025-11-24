"""
API endpoint for receiving Pub/Sub push subscription messages.
This is the webhook endpoint that Google Cloud Pub/Sub calls.
Also includes the cron trigger endpoint for scheduling company sync.
"""
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.logs import setup_logging
from app.dependencies.sync_services import get_pubsub_handler, get_cron_dispatcher

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="")


@router.post(
    "/pubsub-webhook",
    summary="Pub/Sub Webhook Endpoint",
    description="Receives push messages from Google Cloud Pub/Sub subscriptions.",
    responses={
        204: {"description": "Message processed successfully"},
        400: {"description": "Invalid message format"},
        500: {"description": "Internal server error"},
    },
)
async def handle_pubsub_message(
    body: dict[str, Any],
    pubsub_handler=Depends(get_pubsub_handler),
) -> Response:
    """
    Handle incoming Pub/Sub push messages.

    This endpoint receives push messages from Cloud Pub/Sub and processes them.
    It automatically acknowledges the message by returning 2xx status code.

    Args:
        body: The request body containing the Pub/Sub message
        pubsub_handler: PubSubHandler instance (injected)

    Returns:
        204 No Content response to acknowledge the message

    Raises:
        HTTPException: If message processing fails
    """
    try:
        logger.info("Received Pub/Sub message", extra={"body": body})

        # Decode the Pub/Sub message
        try:
            message_payload = pubsub_handler.decode_pubsub_message(body)
        except ValueError as e:
            logger.error(f"Invalid message format: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

        # Process the message
        try:
            result = await pubsub_handler.handle_message(message_payload)
            logger.info(
                "Message processed successfully",
                extra={"result": result},
            )
        except ValueError as e:
            logger.error(f"Unknown action: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(
                f"Message processing error: {str(e)}",
                extra={"error": str(e)},
                exc_info=True,
            )
            raise HTTPException(status_code=500, detail=str(e))

        # Return 204 No Content to acknowledge the message
        # Pub/Sub requires a 2xx response to mark the message as delivered
        return Response(status_code=204)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error handling Pub/Sub message: {str(e)}",
            extra={"error": str(e)},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/scheduler/sync-company-weekly",
    summary="Weekly Company Sync Trigger",
    description="Triggered by Cloud Scheduler to dispatch weekly company batch sync.",
    responses={
        200: {"description": "Sync dispatched successfully"},
        500: {"description": "Internal server error"},
    },
)
async def trigger_weekly_company_sync(
    cron_dispatcher=Depends(get_cron_dispatcher),
) -> dict[str, Any]:
    """
    Trigger weekly company batch sync.

    This endpoint is called by Cloud Scheduler on a weekly basis.
    It fetches all companies from the database, batches them,
    and publishes the batches to the Pub/Sub topic for processing.

    Args:
        cron_dispatcher: CronDispatcher instance (injected)

    Returns:
        Dictionary containing dispatch status and statistics

    Raises:
        HTTPException: If dispatch fails
    """
    try:
        logger.info("Weekly company sync triggered by Cloud Scheduler")

        result = cron_dispatcher.dispatch_weekly_company_sync(batch_size=10)

        logger.info(
            "Weekly company sync dispatched successfully",
            extra=result,
        )

        return result

    except Exception as e:
        logger.error(
            f"Failed to dispatch weekly company sync: {str(e)}",
            extra={"error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to dispatch weekly company sync: {str(e)}",
        )


@router.get(
    "/health",
    summary="Health Check",
    description="Health check endpoint for the Pub/Sub webhook.",
)
def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Status message
    """
    return {"status": "healthy"}
