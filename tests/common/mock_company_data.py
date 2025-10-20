from typing import Type, TypeVar, Any, Dict
from unittest.mock import Mock, PropertyMock
from sqlalchemy.orm import Session

from app.db.models.company import Company
from app.schemas.company import CompanyRead, CompanyWrite

T = TypeVar("T")


class MockCompanyDataBuilder:
    """Builder for creating test data for company with minimal duplication."""

    # Define default data
    _COMPANY_DEFAULTS = {
        "symbol": "TEST",
        "company_name": "Test Company Inc.",
        "price": 100.0,
        "market_cap": 1000000000,
        "currency": "USD",
        "exchange_full_name": "Test Exchange",
        "exchange": "TEST",
        "industry": "Technology",
        "website": "https://test.com",
        "description": "A test company for unit testing.",
        "sector": "Technology",
        "country": "United States",
        "phone": "1-800-TEST",
        "address": "123 Test St",
        "city": "Test City",
        "state": "Test State",
        "zip": "12345",
        "image": "https://test.com/logo.png",
        "ipo_date": "2020-01-01",
    }

    _COMPANY_READ_EXTRA = {
        "id": 1,
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

    @staticmethod
    def _create_mock(defaults: Dict[str, Any], overrides: Dict[str, Any]) -> Mock:
        """
        Create a mock Company object with PropertyMock attributes.

        Args:
            defaults: Default values for the mock
            overrides: Values to override defaults

        Returns:
            Mock company object with configured attributes
        """
        data = {**defaults, **overrides}
        mock_company = Mock(spec=Company)

        # Set attributes using PropertyMock for proper attribute access
        for key, value in data.items():
            setattr(type(mock_company), key, PropertyMock(return_value=value))

        # Add common mock methods
        mock_company.to_dict = Mock(return_value=data)
        mock_company.refresh_from_db = Mock(return_value=None)

        return mock_company

    # ===== Company Mock (for unit tests) =====
    @staticmethod
    def company_mock(**overrides) -> Mock:
        """
        Create a mock Company with default values that can be overridden.

        Useful for unit testing without database interaction.
        Mock objects allow setting relationships without SQLAlchemy constraints.

        Args:
            **overrides: Override default values for any company attributes

        Returns:
            Mock: Configured mock company object

        Examples:
            >>> mock = MockCompanyDataBuilder.company_mock(symbol="AAPL", price=150.0)
            >>> mock.grading_summary = Mock()  # Can freely set relationships
            >>> assert mock.symbol == "AAPL"
        """
        defaults = {
            **MockCompanyDataBuilder._COMPANY_DEFAULTS,
            **MockCompanyDataBuilder._COMPANY_READ_EXTRA,
        }
        return MockCompanyDataBuilder._create_mock(defaults, overrides)

    # ===== Company Model (SQLAlchemy) =====
    @staticmethod
    def company_model(**overrides) -> Company:
        """
        Create a Company model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Note: Setting relationships on real models requires proper setup.

        Args:
            **overrides: Override default values for any company attributes

        Returns:
            Company: SQLAlchemy model instance

        Examples:
            >>> company = MockCompanyDataBuilder.company_model(symbol="AAPL")
            >>> assert isinstance(company, Company)
        """
        return MockCompanyDataBuilder._create_model(
            Company, MockCompanyDataBuilder._COMPANY_DEFAULTS, overrides
        )

    # ===== Company Write Schema (Pydantic) =====
    @staticmethod
    def company_write(**overrides) -> CompanyWrite:
        """
        Create a CompanyWrite schema instance.

        Use for testing API endpoints that accept company data.

        Args:
            **overrides: Override default values for any company attributes

        Returns:
            CompanyWrite: Pydantic schema for API input

        Examples:
            >>> write_schema = MockCompanyDataBuilder.company_write(symbol="AAPL")
            >>> assert isinstance(write_schema, CompanyWrite)
        """
        return MockCompanyDataBuilder._create_schema(
            CompanyWrite, MockCompanyDataBuilder._COMPANY_DEFAULTS, overrides
        )

    # ===== Company Read Schema (Pydantic) =====
    @staticmethod
    def company_read(**overrides) -> CompanyRead:
        """
        Create a CompanyRead schema instance.

        Use for testing API responses that return company data.

        Args:
            **overrides: Override default values for any company attributes

        Returns:
            CompanyRead: Pydantic schema for API output

        Examples:
            >>> read_schema = MockCompanyDataBuilder.company_read(symbol="AAPL")
            >>> assert isinstance(read_schema, CompanyRead)
            >>> assert hasattr(read_schema, 'id')
        """
        defaults = {
            **MockCompanyDataBuilder._COMPANY_DEFAULTS,
            **MockCompanyDataBuilder._COMPANY_READ_EXTRA,
        }
        return MockCompanyDataBuilder._create_schema(CompanyRead, defaults, overrides)

    # ===== Save to Database (for integration tests) =====
    @staticmethod
    def save_company(db_session: Session, **overrides) -> Company:
        """
        Save Company to database.

        Use for integration tests that require database persistence.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any company attributes

        Returns:
            Company: Saved and refreshed SQLAlchemy model

        Examples:
            >>> company = MockCompanyDataBuilder.save_company(db_session, symbol="AAPL")
            >>> assert company.id is not None  # ID assigned by database
        """
        return MockCompanyDataBuilder._save_to_db(
            db_session, Company, MockCompanyDataBuilder._COMPANY_DEFAULTS, overrides
        )
