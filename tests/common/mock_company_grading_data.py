from typing import Type, TypeVar, Any, Dict
from sqlalchemy.orm import Session

from app.schemas.grading import CompanyGradingRead, CompanyGradingSummaryRead
from app.db.models.grading import CompanyGrading, CompanyGradingSummary

T = TypeVar("T")


class MockCompanyGradingDataBuilder:
    """Builder for creating test data for company grading with minimal duplication."""

    # Define default data for each type
    _GRADING_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "grade": "A",
        "score": 85.5,
        "recommendation": "BUY",
        "date": "2023-10-01",
        "created_at": "2023-10-01T00:00:00Z",
        "updated_at": "2023-10-01T00:00:00Z",
    }

    _GRADING_SUMMARY_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "strong_buy": 5,
        "buy": 3,
        "hold": 1,
        "sell": 0,
        "strong_sell": 0,
        "consensus": "Strong Buy",
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

    # ===== Company Grading =====
    @staticmethod
    def company_grading_model(**overrides) -> CompanyGrading:
        """
        Create a CompanyGrading model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Includes grade, score, and recommendation data for a company.

        Args:
            **overrides: Override default values for any grading attributes.
                Common overrides: symbol, grade, score, recommendation, date

        Returns:
            CompanyGrading: SQLAlchemy model instance

        Examples:
            >>> grading = MockCompanyGradingDataBuilder.company_grading_model(
            ...     symbol="AAPL",
            ...     grade="A+",
            ...     score=95.0
            ... )
            >>> assert isinstance(grading, CompanyGrading)
            >>> assert grading.grade == "A+"
        """
        return MockCompanyGradingDataBuilder._create_model(
            CompanyGrading, MockCompanyGradingDataBuilder._GRADING_DEFAULTS, overrides
        )

    @staticmethod
    def company_grading_read(**overrides) -> CompanyGradingRead:
        """
        Create a CompanyGradingRead schema instance.

        Use for testing API responses that return company grading data.
        Includes all fields from the model plus any computed/derived fields.

        Args:
            **overrides: Override default values for any grading attributes.
                Common overrides: symbol, grade, score, recommendation, date

        Returns:
            CompanyGradingRead: Pydantic schema for API output

        Examples:
            >>> grading_read = MockCompanyGradingDataBuilder.company_grading_read(
            ...     symbol="GOOGL",
            ...     recommendation="STRONG BUY"
            ... )
            >>> assert isinstance(grading_read, CompanyGradingRead)
            >>> assert grading_read.recommendation == "STRONG BUY"
        """
        return MockCompanyGradingDataBuilder._create_schema(
            CompanyGradingRead,
            MockCompanyGradingDataBuilder._GRADING_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_company_grading(db_session: Session, **overrides) -> CompanyGrading:
        """
        Save CompanyGrading to database.

        Use for integration tests that require database persistence.
        Automatically removes auto-generated fields (id, timestamps) before insertion.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any grading attributes.
                Common overrides: symbol, grade, score, recommendation, date

        Returns:
            CompanyGrading: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> grading = MockCompanyGradingDataBuilder.save_company_grading(
            ...     db_session,
            ...     symbol="MSFT",
            ...     grade="B+",
            ...     score=82.5
            ... )
            >>> assert grading.id is not None  # ID assigned by database
            >>> assert grading.created_at is not None
        """
        return MockCompanyGradingDataBuilder._save_to_db(
            db_session,
            CompanyGrading,
            MockCompanyGradingDataBuilder._GRADING_DEFAULTS,
            overrides,
        )

    # ===== Company Grading Summary =====
    @staticmethod
    def company_grading_summary_model(**overrides) -> CompanyGradingSummary:
        """
        Create a CompanyGradingSummary model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Aggregates analyst recommendations (strong buy, buy, hold, sell, strong sell).

        Args:
            **overrides: Override default values for any summary attributes.
                Common overrides: symbol, strong_buy, buy, hold, sell, strong_sell, consensus

        Returns:
            CompanyGradingSummary: SQLAlchemy model instance

        Examples:
            >>> summary = MockCompanyGradingDataBuilder.company_grading_summary_model(
            ...     symbol="AAPL",
            ...     strong_buy=10,
            ...     buy=5,
            ...     consensus="Strong Buy"
            ... )
            >>> assert isinstance(summary, CompanyGradingSummary)
            >>> assert summary.strong_buy == 10
        """
        return MockCompanyGradingDataBuilder._create_model(
            CompanyGradingSummary,
            MockCompanyGradingDataBuilder._GRADING_SUMMARY_DEFAULTS,
            overrides,
        )

    @staticmethod
    def company_grading_summary_read(**overrides) -> CompanyGradingSummaryRead:
        """
        Create a CompanyGradingSummaryRead schema instance.

        Use for testing API responses that return grading summary data.
        Provides aggregated view of all analyst recommendations for a company.

        Args:
            **overrides: Override default values for any summary attributes.
                Common overrides: symbol, strong_buy, buy, hold, sell, strong_sell, consensus

        Returns:
            CompanyGradingSummaryRead: Pydantic schema for API output

        Examples:
            >>> summary_read = MockCompanyGradingDataBuilder.company_grading_summary_read(
            ...     symbol="TSLA",
            ...     consensus="Hold"
            ... )
            >>> assert isinstance(summary_read, CompanyGradingSummaryRead)
            >>> assert summary_read.consensus == "Hold"
        """
        return MockCompanyGradingDataBuilder._create_schema(
            CompanyGradingSummaryRead,
            MockCompanyGradingDataBuilder._GRADING_SUMMARY_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_company_grading_summary(
        db_session: Session, **overrides
    ) -> CompanyGradingSummary:
        """
        Save CompanyGradingSummary to database.

        Use for integration tests that require database persistence.
        Automatically removes auto-generated fields (id, timestamps) before insertion.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any summary attributes.
                Common overrides: symbol, strong_buy, buy, hold, sell, strong_sell, consensus

        Returns:
            CompanyGradingSummary: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> summary = MockCompanyGradingDataBuilder.save_company_grading_summary(
            ...     db_session,
            ...     symbol="NFLX",
            ...     strong_buy=8,
            ...     buy=4,
            ...     hold=2,
            ...     consensus="Strong Buy"
            ... )
            >>> assert summary.id is not None  # ID assigned by database
            >>> assert summary.strong_buy == 8
        """
        return MockCompanyGradingDataBuilder._save_to_db(
            db_session,
            CompanyGradingSummary,
            MockCompanyGradingDataBuilder._GRADING_SUMMARY_DEFAULTS,
            overrides,
        )
