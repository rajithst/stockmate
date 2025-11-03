"""Base repository class with common patterns and helpers."""

import logging
from typing import Any, Callable, Generic, TypeVar, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository with common query and upsert patterns."""

    def __init__(self, session: Session):
        self._db = session

    def _get_by_id(self, model_class: type[T], record_id: Any) -> T | None:
        """
        Get a single record by primary key ID.

        Args:
            model_class: ORM model class
            record_id: Primary key value

        Returns:
            Record or None if not found
        """
        try:
            return self._db.query(model_class).filter_by(id=record_id).first()
        except SQLAlchemyError as e:
            logger.error(
                f"Error getting {model_class.__name__} with id {record_id}: {e}"
            )
            raise

    def _get_by_field_value(
        self, model_class: type[T], field_name: str, field_value: Any
    ) -> T | None:
        """
        Get a single record by a specific field value.

        Args:
            model_class: ORM model class
            field_name: Name of the field to filter by (e.g., 'username', 'email')
            field_value: Value to match

        Returns:
            Record or None if not found
        """
        try:
            return (
                self._db.query(model_class)
                .filter_by(**{field_name: field_value})
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(
                f"Error getting {model_class.__name__} by {field_name}={field_value}: {e}"
            )
            raise

    def _get_by_filter(
        self,
        model_class: type[T],
        filter_dict: dict[str, Any],
        order_by_desc: Any | None = None,
        skip: int = 0,
        limit: int | None = None,
    ) -> list[T]:
        """
        Generic get records by multiple filter fields with pagination.

        Args:
            model_class: ORM model class
            filter_dict: Dictionary of field names and values to filter by
            order_by_desc: Column to order by descending
            skip: Number of records to skip (offset)
            limit: Maximum number of records

        Returns:
            List of matching records
        """
        try:
            query = self._db.query(model_class).filter_by(**filter_dict)

            if order_by_desc is not None:
                query = query.order_by(order_by_desc.desc())

            if skip > 0:
                query = query.offset(skip)

            if limit is not None:
                query = query.limit(limit)

            return query.all()
        except SQLAlchemyError as e:
            logger.error(
                f"Error querying {model_class.__name__} with filters {filter_dict}: {e}"
            )
            raise

    def _upsert_records(
        self,
        records_in: list[Any],
        model_class: type[T],
        filter_by_fields: Union[dict[str, Any], Callable, None] = None,
        operation_name: str = "upsert",
    ) -> list[T]:
        """
        Generic upsert pattern for multiple records.

        Args:
            records_in: List of Pydantic schema objects to upsert
            model_class: SQLAlchemy model class
            filter_by_fields: One of:
                - Callable: Function that takes a record and returns dict of filter fields
                           (e.g., lambda r: {"id": r.id, "user_id": r.user_id})
                - Dict: Static filter fields for all records
                - None: MUST be callable or dict, raises error if None
            operation_name: Name for logging

        Returns:
            List of persisted ORM models

        Raises:
            ValueError: If filter_by_fields is None
        """
        try:
            if filter_by_fields is None:
                raise ValueError(
                    f"filter_by_fields cannot be None for {operation_name}. "
                    "Provide either a callable or dict with filter fields."
                )

            results = []
            for record_in in records_in:
                # Determine filter fields
                if callable(filter_by_fields):
                    filter_fields = filter_by_fields(record_in)
                else:
                    filter_fields = filter_by_fields

                # Find existing record
                existing = (
                    self._db.query(model_class).filter_by(**filter_fields).first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, record_in)
                else:
                    # Create new
                    result = model_class(**record_in.model_dump(exclude_unset=True))
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during {operation_name}: {e}")
            raise

    def _upsert_single(
        self,
        record_in: Any,
        model_class: type[T],
        filter_by_fields: Union[dict[str, Any], Callable, None] = None,
        operation_name: str = "upsert",
    ) -> T:
        """
        Generic upsert pattern for a single record.

        Args:
            record_in: Pydantic schema object to upsert
            model_class: SQLAlchemy model class
            filter_by_fields: One of:
                - Callable: Function that takes the record and returns dict of filter fields
                           (e.g., lambda r: {"id": r.id})
                - Dict: Static filter fields (e.g., {"symbol": "AAPL"})
                - None: MUST be callable or dict, raises error if None
            operation_name: Name for logging

        Returns:
            Persisted ORM model

        Raises:
            ValueError: If filter_by_fields is None
        """
        try:
            if filter_by_fields is None:
                raise ValueError(
                    f"filter_by_fields cannot be None for {operation_name}. "
                    "Provide either a callable or dict with filter fields."
                )

            # Determine filter fields
            if callable(filter_by_fields):
                filter_fields = filter_by_fields(record_in)
            else:
                filter_fields = filter_by_fields

            existing = self._db.query(model_class).filter_by(**filter_fields).first()

            if existing:
                result = map_model(existing, record_in)
            else:
                result = model_class(**record_in.model_dump(exclude_unset=True))
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during {operation_name}: {e}")
            raise

    def _delete_by_filter(
        self,
        model_class: type[T],
        filter_dict: dict[str, Any],
        operation_name: str = "delete",
    ) -> bool:
        """
        Generic delete pattern by filter fields.

        Args:
            model_class: ORM model class
            filter_dict: Dictionary of field names and values to filter by
            operation_name: Name for logging

        Returns:
            True if deleted, False if not found
        """
        try:
            record = self._db.query(model_class).filter_by(**filter_dict).first()

            if record:
                self._db.delete(record)
                self._db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during {operation_name}: {e}")
            raise

    def _delete_by_join(
        self,
        model_class: type[T],
        join_model: type,
        filter_conditions: list,
        operation_name: str = "delete",
    ) -> bool:
        """
        Generic delete pattern with join and multiple filter conditions.

        Args:
            model_class: ORM model class to delete from
            join_model: ORM model class to join with
            filter_conditions: List of SQLAlchemy filter conditions
            operation_name: Name for logging

        Returns:
            True if deleted, False if not found
        """
        try:
            query = self._db.query(model_class).join(join_model)
            for condition in filter_conditions:
                query = query.filter(condition)

            record = query.first()

            if record:
                self._db.delete(record)
                self._db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during {operation_name}: {e}")
            raise
