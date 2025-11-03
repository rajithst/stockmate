"""
Base sync service for all FMP API integrations.

Provides common patterns for:
- Company lookup and validation
- API response validation
- Schema transformations
- Error handling and logging
- Database persistence orchestration
"""

import logging
from typing import Any, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.db.models.company import Company
from app.repositories.company_repo import CompanyRepository

logger = logging.getLogger(__name__)

T = TypeVar("T")
SchemaWrite = TypeVar("SchemaWrite")
SchemaRead = TypeVar("SchemaRead")


class BaseSyncService:
    """
    Base class for all FMP API sync services with common patterns.

    Each sync service (MetricsSyncService, FinancialSyncService, etc.)
    inherits from this class to eliminate boilerplate code for:
    - Company lookups
    - API response validation
    - Schema transformations
    - Error handling
    - Logging

    Usage:
        class MyService(BaseSyncService):
            def __init__(self, api_client, session):
                super().__init__(api_client, session)
                self._repository = MyRepository(session)

            def upsert_data(self, symbol):
                return self._sync_data(
                    symbol=symbol,
                    api_method=self._market_api_client.get_data,
                    repo_method=self._repository.upsert_data,
                    schema_write=DataWrite,
                    schema_read=DataRead,
                    data_type_name="data"
                )
    """

    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        """
        Initialize base sync service.

        Args:
            market_api_client: FMP API client
            session: SQLAlchemy session
        """
        self._market_api_client = market_api_client
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

    # ========== DATA VALIDATION ==========

    def _validate_api_response(self, data: Any, data_type: str, symbol: str) -> bool:
        """
        Validate API response is not empty.

        Args:
            data: Response data from API
            data_type: Type of data (e.g., 'key_metrics', 'balance_sheets')
            symbol: Stock symbol

        Returns:
            True if valid, False if empty/None
        """
        if not data:
            logger.info(f"No {data_type} data found for symbol: {symbol}")
            return False
        return True

    # ========== SCHEMA TRANSFORMATIONS ==========

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

    # ========== MONITORING & LOGGING ==========

    def _log_sync_success(self, operation: str, count: int, symbol: str) -> None:
        """
        Log successful sync operation.

        Args:
            operation: Operation name (e.g., 'key_metrics', 'balance_sheets')
            count: Number of records synced
            symbol: Stock symbol
        """
        logger.info(f"Successfully synced {count} {operation} record(s) for {symbol}")

    def _log_sync_failure(self, operation: str, symbol: str, error: Exception) -> None:
        """
        Log failed sync operation.

        Args:
            operation: Operation name (e.g., 'key_metrics', 'balance_sheets')
            symbol: Stock symbol
            error: Exception that occurred
        """
        logger.error(
            f"Error syncing {operation} for {symbol}: {str(error)}", exc_info=True
        )
