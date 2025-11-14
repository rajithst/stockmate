import logging
from typing import Any, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.db.models.company import Company
from app.repositories.company_repo import CompanyRepository

logger = logging.getLogger(__name__)

T = TypeVar("T")
SchemaWrite = TypeVar("SchemaWrite")
SchemaRead = TypeVar("SchemaRead")


class BaseSyncService:
    """Base service for syncing data from FMP to database."""

    def __init__(self, session: Session):
        """
        Initialize base sync service.

        Args:
            session: SQLAlchemy session
        """
        self._company_repository = CompanyRepository(session)
        self._session = session

    # ========== COMPANY LOOKUPS ==========

    def _get_company_or_fail(self, symbol: str) -> Optional[Company]:
        """
        Get company by symbol, logging appropriately.

        Args:
            symbol: Stock symbol (e.g., 'AAPL')

        Returns:
            Company model or None if not found

        Raises:
            Exception: On database error
        """
        try:
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None
            return company
        except Exception as e:
            logger.error(f"Error fetching company {symbol}: {str(e)}", exc_info=True)
            raise

    def _add_company_id_to_records(
        self, records: list, company_id: int, schema_write: Type[SchemaWrite]
    ) -> list[SchemaWrite]:
        """
        Add company_id to records and validate with schema.

        Transforms API response records by injecting company_id and
        validating against the provided Pydantic write schema.

        Args:
            records: List of API response records (with .model_dump() method)
            company_id: Company ID to inject
            schema_write: Pydantic write schema class for validation

        Returns:
            List of validated schema objects

        Raises:
            Exception: On schema validation error
        """
        try:
            return [
                self._add_company_id_to_record(record, company_id, schema_write)
                for record in records
            ]
        except Exception as e:
            logger.error(
                f"Error transforming records to schema: {str(e)}", exc_info=True
            )
            raise

    def _add_company_id_to_record(
        self, record: Any, company_id: int, schema_write: Type[SchemaWrite]
    ) -> SchemaWrite:
        """
        Add company_id to a single record and validate with schema.

        Transforms an API response record by injecting company_id and
        validating against the provided Pydantic write schema.

        Args:
            record: Single API response record (with .model_dump() method)
            company_id: Company ID to inject
            schema_write: Pydantic write schema class for validation

        Returns:
            Validated schema object

        Raises:
            Exception: On schema validation error
        """
        try:
            return schema_write.model_validate(
                {**record.model_dump(), "company_id": company_id}
            )
        except Exception as e:
            logger.error(
                f"Error transforming record to schema: {str(e)}", exc_info=True
            )
            raise

    def _map_schema_list(
        self, records: list, schema_read: Type[SchemaRead]
    ) -> list[SchemaRead]:
        """
        Map list of ORM models to read schemas.

        Args:
            records: List of ORM models from repository
            schema_read: Pydantic read schema class

        Returns:
            List of read schema objects

        Raises:
            Exception: On schema validation error
        """
        try:
            return [self._map_schema_single(record, schema_read) for record in records]
        except Exception as e:
            logger.error(f"Error mapping records to schema: {str(e)}", exc_info=True)
            raise

    def _map_schema_single(
        self, record: Any, schema_read: Type[SchemaRead]
    ) -> SchemaRead:
        """
        Map single ORM model to read schema.

        Args:
            record: Single ORM model from repository
            schema_read: Pydantic read schema class

        Returns:
            Read schema object

        Raises:
            Exception: On schema validation error
        """
        try:
            return schema_read.model_validate(record)
        except Exception as e:
            logger.error(f"Error mapping record to schema: {str(e)}", exc_info=True)
            raise
