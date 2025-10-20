from typing import Type, TypeVar, Any, Dict
from sqlalchemy.orm import Session

from app.schemas.rating import CompanyRatingSummaryRead
from app.db.models.ratings import CompanyRatingSummary

T = TypeVar("T")


class MockCompanyRatingSummaryBuilder:
    """Builder for creating test data for company rating summary with minimal duplication."""

    # Define default data
    _RATING_SUMMARY_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "rating": "Buy",
        "overall_score": 4,
        "discounted_cash_flow_score": 4,
        "return_on_equity_score": 4,
        "return_on_assets_score": 4,
        "debt_to_equity_score": 3,
        "price_to_earnings_score": 4,
        "price_to_book_score": 4,
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

    # ===== Company Rating Summary =====
    @staticmethod
    def company_rating_summary_model(**overrides) -> CompanyRatingSummary:
        """
        Create a CompanyRatingSummary model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Contains overall rating and individual metric scores (ROE, ROA, DCF, P/E, P/B, D/E).
        Scores typically range from 1-5, with 5 being the best.

        Args:
            **overrides: Override default values for any rating summary attributes.
                Common overrides: symbol, rating, overall_score, discounted_cash_flow_score,
                return_on_equity_score, return_on_assets_score, debt_to_equity_score,
                price_to_earnings_score, price_to_book_score

        Returns:
            CompanyRatingSummary: SQLAlchemy model instance

        Examples:
            >>> rating = MockCompanyRatingSummaryBuilder.company_rating_summary_model(
            ...     symbol="AAPL",
            ...     rating="Strong Buy",
            ...     overall_score=5,
            ...     discounted_cash_flow_score=5
            ... )
            >>> assert isinstance(rating, CompanyRatingSummary)
            >>> assert rating.overall_score == 5
            >>> assert rating.rating == "Strong Buy"
        """
        return MockCompanyRatingSummaryBuilder._create_model(
            CompanyRatingSummary,
            MockCompanyRatingSummaryBuilder._RATING_SUMMARY_DEFAULTS,
            overrides,
        )

    @staticmethod
    def company_rating_summary_read(**overrides) -> CompanyRatingSummaryRead:
        """
        Create a CompanyRatingSummaryRead schema instance.

        Use for testing API responses that return company rating summary data.
        Provides aggregated view of all financial metric scores and overall rating.
        Useful for validating API output serialization and data transformations.

        Args:
            **overrides: Override default values for any rating summary attributes.
                Common overrides: symbol, rating, overall_score, discounted_cash_flow_score,
                return_on_equity_score, return_on_assets_score, debt_to_equity_score,
                price_to_earnings_score, price_to_book_score

        Returns:
            CompanyRatingSummaryRead: Pydantic schema for API output

        Examples:
            >>> rating_read = MockCompanyRatingSummaryBuilder.company_rating_summary_read(
            ...     symbol="GOOGL",
            ...     rating="Buy",
            ...     return_on_equity_score=5
            ... )
            >>> assert isinstance(rating_read, CompanyRatingSummaryRead)
            >>> assert rating_read.return_on_equity_score == 5
            >>> assert rating_read.rating == "Buy"
        """
        return MockCompanyRatingSummaryBuilder._create_schema(
            CompanyRatingSummaryRead,
            MockCompanyRatingSummaryBuilder._RATING_SUMMARY_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_company_rating_summary(
        db_session: Session, **overrides
    ) -> CompanyRatingSummary:
        """
        Save CompanyRatingSummary to database.

        Use for integration tests that require database persistence and relationship testing.
        Automatically removes auto-generated fields (id, timestamps) before insertion.
        The saved instance will have DB-assigned ID and timestamps.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any rating summary attributes.
                Common overrides: symbol, rating, overall_score, discounted_cash_flow_score,
                return_on_equity_score, return_on_assets_score, debt_to_equity_score,
                price_to_earnings_score, price_to_book_score

        Returns:
            CompanyRatingSummary: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> rating = MockCompanyRatingSummaryBuilder.save_company_rating_summary(
            ...     db_session,
            ...     symbol="MSFT",
            ...     rating="Strong Buy",
            ...     overall_score=5,
            ...     price_to_earnings_score=4,
            ...     price_to_book_score=4
            ... )
            >>> assert rating.id is not None  # ID assigned by database
            >>> assert rating.created_at is not None
            >>> assert rating.symbol == "MSFT"
            >>> assert rating.overall_score == 5
        """
        return MockCompanyRatingSummaryBuilder._save_to_db(
            db_session,
            CompanyRatingSummary,
            MockCompanyRatingSummaryBuilder._RATING_SUMMARY_DEFAULTS,
            overrides,
        )
