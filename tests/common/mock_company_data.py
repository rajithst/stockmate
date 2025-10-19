from unittest.mock import Mock, PropertyMock

from app.db.models.company import Company
from app.schemas.company import CompanyRead, CompanyWrite


class MockCompanyDataBuilder:
    """Builder class for creating test data with flexible configuration."""

    mock_data = {
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

    # company db model
    @staticmethod
    def company_model(**overrides) -> Mock:
        """
        Create a mock Company with default values that can be overridden.

        Args:
            **kwargs: Override default values for any company attributes

        Returns:
            Mock: Configured mock company object
        """
        defaults = {
            "id": 1,
            "symbol": "TEST",
            "name": "Test Company",
            "sector": "Technology",
            "industry": "Software",
            "description": "Test company description",
        }

        data = {**defaults, **overrides}
        mock_company = Mock(spec=Company)

        for key, value in data.items():
            setattr(type(mock_company), key, PropertyMock(return_value=value))

        mock_company.to_dict = Mock(return_value=data)
        mock_company.refresh_from_db = Mock(return_value=None)

        return mock_company

    @staticmethod
    def company_write(**overrides) -> CompanyWrite:
        """Build CompanyWrite test data with optional overrides."""
        default_data = MockCompanyDataBuilder.mock_data.copy()
        return CompanyWrite(**(default_data | overrides))

    @staticmethod
    def company_read(**overrides) -> CompanyRead:
        """Build CompanyRead test data with optional overrides."""
        default_data = MockCompanyDataBuilder.mock_data.copy()
        default_data.update(
            {
                "id": 1,
                "created_at": "2023-10-01T00:00:00Z",
                "updated_at": "2023-10-01T00:00:00Z",
            }
        )
        return CompanyRead(**(default_data | overrides))

    # save test data in test db for integration tests
    @staticmethod
    def save_company(db_session, **overrides) -> Company:
        """Create and save a Company instance in the test database."""

        default_data = MockCompanyDataBuilder.mock_data.copy()
        company = Company(**default_data | overrides)
        db_session.add(company)
        db_session.commit()
        db_session.refresh(company)
        return company
