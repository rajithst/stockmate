from typing import Type, TypeVar, Any, Dict
from sqlalchemy.orm import Session

from app.schemas.quote import StockPriceChangeRead
from app.db.models.quote import StockPriceChange

T = TypeVar("T")


class MockStockPriceChangeDataBuilder:
    """Builder for creating test data for stock price changes with minimal duplication."""

    # Define default data
    _PRICE_CHANGE_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "AAPL",
        "one_day": 2.5,
        "five_day": 3.0,
        "one_month": 5.0,
        "three_month": 7.5,
        "six_month": 10.0,
        "ytd": 12.0,
        "one_year": 15.0,
        "three_year": 25.0,
        "five_year": 40.0,
        "ten_year": 80.0,
        "created_at": "2023-10-01T00:00:00Z",
        "updated_at": "2023-10-01T00:00:00Z",
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

    # ===== Stock Price Change =====
    @staticmethod
    def stock_price_change_model(**overrides) -> StockPriceChange:
        """
        Create a StockPriceChange model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Tracks historical price performance across multiple timeframes (1 day to 10 years).
        All values represent percentage changes from the starting price in each period.

        Args:
            **overrides: Override default values for any price change attributes.
                Common overrides: symbol, one_day, five_day, one_month, three_month,
                six_month, ytd, one_year, three_year, five_year, ten_year

        Returns:
            StockPriceChange: SQLAlchemy model instance

        Examples:
            >>> price_change = MockStockPriceChangeDataBuilder.stock_price_change_model(
            ...     symbol="AAPL",
            ...     one_day=1.5,
            ...     one_month=8.0,
            ...     one_year=25.0
            ... )
            >>> assert isinstance(price_change, StockPriceChange)
            >>> assert price_change.one_year > price_change.one_month  # Long-term gain
            >>> assert price_change.symbol == "AAPL"
        """
        return MockStockPriceChangeDataBuilder._create_model(
            StockPriceChange,
            MockStockPriceChangeDataBuilder._PRICE_CHANGE_DEFAULTS,
            overrides,
        )

    @staticmethod
    def stock_price_change_read(**overrides) -> StockPriceChangeRead:
        """
        Create a StockPriceChangeRead schema instance.

        Use for testing API responses that return stock price change data.
        Provides comprehensive view of stock performance across all timeframes.
        Useful for displaying price trends, momentum analysis, and performance charts.

        Args:
            **overrides: Override default values for any price change attributes.
                Common overrides: symbol, one_day, five_day, one_month, three_month,
                six_month, ytd, one_year, three_year, five_year, ten_year

        Returns:
            StockPriceChangeRead: Pydantic schema for API output

        Examples:
            >>> price_change_read = MockStockPriceChangeDataBuilder.stock_price_change_read(
            ...     symbol="TSLA",
            ...     one_day=-2.5,
            ...     ytd=45.0,
            ...     five_year=150.0
            ... )
            >>> assert isinstance(price_change_read, StockPriceChangeRead)
            >>> assert price_change_read.one_day < 0  # Daily decline
            >>> assert price_change_read.five_year > 0  # Long-term growth
            >>> assert price_change_read.symbol == "TSLA"
        """
        return MockStockPriceChangeDataBuilder._create_schema(
            StockPriceChangeRead,
            MockStockPriceChangeDataBuilder._PRICE_CHANGE_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_stock_price_change(db_session: Session, **overrides) -> StockPriceChange:
        """
        Save StockPriceChange to database.

        Use for integration tests that require database persistence and relationship testing.
        Automatically removes auto-generated fields (id, timestamps) before insertion.
        The saved instance will have DB-assigned ID and timestamps for tracking updates.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any price change attributes.
                Common overrides: symbol, one_day, five_day, one_month, three_month,
                six_month, ytd, one_year, three_year, five_year, ten_year

        Returns:
            StockPriceChange: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> price_change = MockStockPriceChangeDataBuilder.save_stock_price_change(
            ...     db_session,
            ...     symbol="GOOGL",
            ...     one_day=0.5,
            ...     one_month=4.2,
            ...     ytd=18.5,
            ...     one_year=22.0,
            ...     five_year=95.0
            ... )
            >>> assert price_change.id is not None  # ID assigned by database
            >>> assert price_change.created_at is not None
            >>> assert price_change.symbol == "GOOGL"
            >>> assert price_change.ytd == 18.5
            >>> # Positive values across all periods indicate consistent growth
        """
        return MockStockPriceChangeDataBuilder._save_to_db(
            db_session,
            StockPriceChange,
            MockStockPriceChangeDataBuilder._PRICE_CHANGE_DEFAULTS,
            overrides,
        )
