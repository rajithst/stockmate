import logging


def setup_logging():
    """Setup logging configuration with proper SQLAlchemy query logging."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    # Configure SQLAlchemy logging (only show INFO level queries)
    # This logs SQL statements without duplicates
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.pool").setLevel(
        logging.WARNING
    )  # Suppress pool debug logs
