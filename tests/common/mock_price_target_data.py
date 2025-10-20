from typing import Type, TypeVar, Any, Dict
from sqlalchemy.orm import Session

from app.schemas.price_target import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary

T = TypeVar("T")


class MockPriceTargetDataBuilder:
    """Builder for creating test data for price targets with minimal duplication."""

    # Define default data for each type
    _PRICE_TARGET_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "target_high": 150.0,
        "target_low": 100.0,
        "target_consensus": 125.0,
        "target_median": 130.0,
        "created_at": "2023-10-01T00:00:00",
        "updated_at": "2023-10-01T00:00:00",
    }

    _PRICE_TARGET_SUMMARY_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "last_month_count": 5,
        "last_month_average_price_target": 128.0,
        "last_quarter_count": 15,
        "last_quarter_average_price_target": 130.0,
        "last_year_count": 60,
        "last_year_average_price_target": 127.5,
        "all_time_count": 200,
        "all_time_average_price_target": 125.0,
        "publishers": "Analyst A, Analyst B",
        "created_at": "2023-10-01T00:00:00",
        "updated_at": "2023-10-01T00:00:00",
    }

    @staticmethod
    def _create_model(
        model_class: Type[T], defaults: Dict[str, Any], overrides: Dict[str, Any]
    ) -> T:
        """
        Generic method to create a model instance.

        Args:
            model_class: The SQLAlchemy model class to instantiate
            defaults: Default values for the model
            overrides: Values to override defaults

        Returns:
            Model instance with merged data
        """
        data = {**defaults, **overrides}
        model = model_class(**data)
        # Manually set id since it's usually auto-generated
        if "id" in data:
            model.id = data["id"]
        return model

    @staticmethod
    def _create_schema(
        schema_class: Type[T], defaults: Dict[str, Any], overrides: Dict[str, Any]
    ) -> T:
        """
        Generic method to create a Pydantic schema instance.

        Args:
            schema_class: The Pydantic schema class to instantiate
            defaults: Default values for the schema
            overrides: Values to override defaults

        Returns:
            Schema instance with merged data
        """
        return schema_class(**(defaults | overrides))

    @staticmethod
    def _save_to_db(
        db_session: Session,
        model_class: Type[T],
        defaults: Dict[str, Any],
        overrides: Dict[str, Any],
    ) -> T:
        """
        Generic method to save a model to database.

        Args:
            db_session: Database session
            model_class: The SQLAlchemy model class to instantiate
            defaults: Default values for the model
            overrides: Values to override defaults

        Returns:
            Saved and refreshed model instance
        """
        # Remove fields that shouldn't be set when creating
        data = {**defaults, **overrides}
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        model = model_class(**data)
        db_session.add(model)
        db_session.commit()
        db_session.refresh(model)
        return model

    # ===== Price Target =====
    @staticmethod
    def price_target_model(**overrides) -> CompanyPriceTarget:
        """
        Create a CompanyPriceTarget model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Contains analyst price target range (high, low, consensus, median) for a stock.
        Price targets help investors gauge analyst expectations for future stock price.

        Args:
            **overrides: Override default values for any price target attributes.
                Common overrides: symbol, target_high, target_low, target_consensus,
                target_median

        Returns:
            CompanyPriceTarget: SQLAlchemy model instance

        Examples:
            >>> price_target = MockPriceTargetDataBuilder.price_target_model(
            ...     symbol="AAPL",
            ...     target_high=180.0,
            ...     target_low=140.0,
            ...     target_consensus=165.0
            ... )
            >>> assert isinstance(price_target, CompanyPriceTarget)
            >>> assert price_target.target_high > price_target.target_low
            >>> assert price_target.symbol == "AAPL"
        """
        return MockPriceTargetDataBuilder._create_model(
            CompanyPriceTarget,
            MockPriceTargetDataBuilder._PRICE_TARGET_DEFAULTS,
            overrides,
        )

    @staticmethod
    def price_target_read(**overrides) -> CompanyPriceTargetRead:
        """
        Create a CompanyPriceTargetRead schema instance.

        Use for testing API responses that return price target data.
        Provides analyst consensus on expected future stock price levels.
        Useful for displaying target range, median, and consensus in UI.

        Args:
            **overrides: Override default values for any price target attributes.
                Common overrides: symbol, target_high, target_low, target_consensus,
                target_median

        Returns:
            CompanyPriceTargetRead: Pydantic schema for API output

        Examples:
            >>> price_target_read = MockPriceTargetDataBuilder.price_target_read(
            ...     symbol="TSLA",
            ...     target_high=300.0,
            ...     target_low=200.0,
            ...     target_median=250.0
            ... )
            >>> assert isinstance(price_target_read, CompanyPriceTargetRead)
            >>> assert price_target_read.target_median == 250.0
            >>> # Median between high and low indicates balanced analyst views
        """
        return MockPriceTargetDataBuilder._create_schema(
            CompanyPriceTargetRead,
            MockPriceTargetDataBuilder._PRICE_TARGET_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_price_target(db_session: Session, **overrides) -> CompanyPriceTarget:
        """
        Save CompanyPriceTarget to database.

        Use for integration tests that require database persistence and relationship testing.
        Automatically removes auto-generated fields (id, timestamps) before insertion.
        The saved instance will have DB-assigned ID and timestamps.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any price target attributes.
                Common overrides: symbol, target_high, target_low, target_consensus,
                target_median

        Returns:
            CompanyPriceTarget: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> price_target = MockPriceTargetDataBuilder.save_price_target(
            ...     db_session,
            ...     symbol="GOOGL",
            ...     target_high=2900.0,
            ...     target_low=2400.0,
            ...     target_consensus=2650.0,
            ...     target_median=2700.0
            ... )
            >>> assert price_target.id is not None  # ID assigned by database
            >>> assert price_target.created_at is not None
            >>> assert price_target.symbol == "GOOGL"
        """
        return MockPriceTargetDataBuilder._save_to_db(
            db_session,
            CompanyPriceTarget,
            MockPriceTargetDataBuilder._PRICE_TARGET_DEFAULTS,
            overrides,
        )

    # ===== Price Target Summary =====
    @staticmethod
    def price_target_summary_model(**overrides) -> CompanyPriceTargetSummary:
        """
        Create a CompanyPriceTargetSummary model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Aggregates analyst price targets over different time periods (month, quarter, year, all-time).
        Tracks number of analysts and average price targets for trend analysis.

        Args:
            **overrides: Override default values for any price target summary attributes.
                Common overrides: symbol, last_month_count, last_month_average_price_target,
                last_quarter_count, last_quarter_average_price_target, last_year_count,
                last_year_average_price_target, all_time_count, all_time_average_price_target,
                publishers

        Returns:
            CompanyPriceTargetSummary: SQLAlchemy model instance

        Examples:
            >>> summary = MockPriceTargetDataBuilder.price_target_summary_model(
            ...     symbol="AAPL",
            ...     last_month_count=8,
            ...     last_month_average_price_target=175.0,
            ...     last_quarter_count=25,
            ...     last_quarter_average_price_target=172.0
            ... )
            >>> assert isinstance(summary, CompanyPriceTargetSummary)
            >>> assert summary.last_month_count == 8
            >>> assert summary.last_month_average_price_target > 0
        """
        return MockPriceTargetDataBuilder._create_model(
            CompanyPriceTargetSummary,
            MockPriceTargetDataBuilder._PRICE_TARGET_SUMMARY_DEFAULTS,
            overrides,
        )

    @staticmethod
    def price_target_summary_read(**overrides) -> CompanyPriceTargetSummaryRead:
        """
        Create a CompanyPriceTargetSummaryRead schema instance.

        Use for testing API responses that return price target summary data.
        Shows historical analyst activity and price target trends over time.
        Helps identify if analyst sentiment is improving or declining.

        Args:
            **overrides: Override default values for any price target summary attributes.
                Common overrides: symbol, last_month_count, last_month_average_price_target,
                last_quarter_count, last_quarter_average_price_target, last_year_count,
                last_year_average_price_target, all_time_count, all_time_average_price_target,
                publishers

        Returns:
            CompanyPriceTargetSummaryRead: Pydantic schema for API output

        Examples:
            >>> summary_read = MockPriceTargetDataBuilder.price_target_summary_read(
            ...     symbol="MSFT",
            ...     last_month_count=10,
            ...     last_month_average_price_target=380.0,
            ...     last_year_count=75,
            ...     last_year_average_price_target=350.0
            ... )
            >>> assert isinstance(summary_read, CompanyPriceTargetSummaryRead)
            >>> # Rising average indicates improving analyst sentiment
            >>> assert summary_read.last_month_average_price_target > summary_read.last_year_average_price_target
        """
        return MockPriceTargetDataBuilder._create_schema(
            CompanyPriceTargetSummaryRead,
            MockPriceTargetDataBuilder._PRICE_TARGET_SUMMARY_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_price_target_summary(
        db_session: Session, **overrides
    ) -> CompanyPriceTargetSummary:
        """
        Save CompanyPriceTargetSummary to database.

        Use for integration tests that require database persistence and relationship testing.
        Automatically removes auto-generated fields (id, timestamps) before insertion.
        Useful for testing time-series analysis of analyst sentiment changes.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any price target summary attributes.
                Common overrides: symbol, last_month_count, last_month_average_price_target,
                last_quarter_count, last_quarter_average_price_target, last_year_count,
                last_year_average_price_target, all_time_count, all_time_average_price_target,
                publishers

        Returns:
            CompanyPriceTargetSummary: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> summary = MockPriceTargetDataBuilder.save_price_target_summary(
            ...     db_session,
            ...     symbol="NFLX",
            ...     last_month_count=6,
            ...     last_month_average_price_target=520.0,
            ...     last_quarter_count=18,
            ...     last_quarter_average_price_target=510.0,
            ...     publishers="Morgan Stanley, Goldman Sachs, JP Morgan"
            ... )
            >>> assert summary.id is not None  # ID assigned by database
            >>> assert summary.last_month_count == 6
            >>> assert "Morgan Stanley" in summary.publishers
        """
        return MockPriceTargetDataBuilder._save_to_db(
            db_session,
            CompanyPriceTargetSummary,
            MockPriceTargetDataBuilder._PRICE_TARGET_SUMMARY_DEFAULTS,
            overrides,
        )
