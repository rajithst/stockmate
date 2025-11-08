from typing import Type, TypeVar, Any, Dict
from sqlalchemy.orm import Session

from app.schemas.company_metrics import CompanyDiscountedCashFlowRead
from app.db.models.dcf import DiscountedCashFlow

T = TypeVar("T")


class MockDiscountedCashFlowDataBuilder:
    """Builder for creating test data for discounted cash flow with minimal duplication."""

    # Define default data
    _DCF_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "date": "2023-10-01",
        "dcf": 175.0,
        "stock_price": 160.0,
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

    # ===== Discounted Cash Flow =====
    @staticmethod
    def discounted_cash_flow_model(**overrides) -> DiscountedCashFlow:
        """
        Create a DiscountedCashFlow model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        DCF represents the intrinsic value of a company based on projected future cash flows.
        Compare DCF value with stock price to determine if stock is undervalued or overvalued.

        Args:
            **overrides: Override default values for any DCF attributes.
                Common overrides: symbol, dcf (intrinsic value), stock_price (market price),
                date (valuation date)

        Returns:
            DiscountedCashFlow: SQLAlchemy model instance

        Examples:
            >>> dcf = MockDiscountedCashFlowDataBuilder.discounted_cash_flow_model(
            ...     symbol="AAPL",
            ...     dcf=180.0,
            ...     stock_price=150.0
            ... )
            >>> assert isinstance(dcf, DiscountedCashFlow)
            >>> assert dcf.dcf > dcf.stock_price  # Stock is undervalued
            >>> assert dcf.symbol == "AAPL"
        """
        return MockDiscountedCashFlowDataBuilder._create_model(
            DiscountedCashFlow,
            MockDiscountedCashFlowDataBuilder._DCF_DEFAULTS,
            overrides,
        )

    @staticmethod
    def discounted_cash_flow_read(**overrides) -> CompanyDiscountedCashFlowRead:
        """
        Create a CompanyDiscountedCashFlowRead schema instance.

        Use for testing API responses that return DCF valuation data.
        Provides intrinsic value calculation compared to current market price.
        Helps investors identify potentially undervalued or overvalued stocks.

        Args:
            **overrides: Override default values for any DCF attributes.
                Common overrides: symbol, dcf (intrinsic value), stock_price (market price),
                date (valuation date)

        Returns:
            CompanyDiscountedCashFlowRead: Pydantic schema for API output

        Examples:
            >>> dcf_read = MockDiscountedCashFlowDataBuilder.discounted_cash_flow_read(
            ...     symbol="GOOGL",
            ...     dcf=2500.0,
            ...     stock_price=2800.0
            ... )
            >>> assert isinstance(dcf_read, CompanyDiscountedCashFlowRead)
            >>> assert dcf_read.dcf < dcf_read.stock_price  # Stock is overvalued
            >>> assert dcf_read.symbol == "GOOGL"
        """
        return MockDiscountedCashFlowDataBuilder._create_schema(
            CompanyDiscountedCashFlowRead,
            MockDiscountedCashFlowDataBuilder._DCF_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_discounted_cash_flow(
        db_session: Session, **overrides
    ) -> DiscountedCashFlow:
        """
        Save DiscountedCashFlow to database.

        Use for integration tests that require database persistence and relationship testing.
        Automatically removes auto-generated fields (id, timestamps) before insertion.
        The saved instance will have DB-assigned ID and timestamps.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any DCF attributes.
                Common overrides: symbol, dcf (intrinsic value), stock_price (market price),
                date (valuation date)

        Returns:
            DiscountedCashFlow: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> dcf = MockDiscountedCashFlowDataBuilder.save_discounted_cash_flow(
            ...     db_session,
            ...     symbol="MSFT",
            ...     dcf=350.0,
            ...     stock_price=330.0,
            ...     date="2023-12-01"
            ... )
            >>> assert dcf.id is not None  # ID assigned by database
            >>> assert dcf.created_at is not None
            >>> assert dcf.symbol == "MSFT"
            >>> assert dcf.dcf == 350.0
            >>> # DCF > stock_price indicates stock is undervalued
        """
        return MockDiscountedCashFlowDataBuilder._save_to_db(
            db_session,
            DiscountedCashFlow,
            MockDiscountedCashFlowDataBuilder._DCF_DEFAULTS,
            overrides,
        )
