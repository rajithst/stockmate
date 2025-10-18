from unittest.mock import Mock, PropertyMock

from app.db.models.company import Company
from app.schemas.company import CompanyPageResponse, CompanyRead, CompanyWrite
from app.schemas.grading import CompanyGradingRead
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)


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

    relationships = {
        "dividends": [],
        "stock_splits": [],
        "income_statements": [],
        "balance_sheets": [],
        "cash_flow_statements": [],
        "ratings": [],
        "gradings": [],
        "grading_summary": None,
        "discounted_cash_flow": None,
        "financial_score": None,
        "general_news": [],
        "price_target_news": [],
        "grading_news": [],
        "key_metrics": [],
        "financial_ratios": [],
        "stock_peers": [],
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
        default_data.update(overrides)
        return CompanyWrite(**default_data)

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
        default_data.update(overrides)
        return CompanyRead(**default_data)

    @staticmethod
    def company_grading_read(**overrides) -> CompanyGradingRead:
        """Build CompanyGradingRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "grade": "A",
            "score": 85.5,
            "recommendation": "BUY",
            "date": "2023-10-01",
        }
        default_data.update(overrides)
        return CompanyGradingRead(**default_data)

    @staticmethod
    def company_page_response(**overrides) -> CompanyPageResponse:
        """Build complete CompanyPageResponse test data."""
        defaults = {
            "company": MockCompanyDataBuilder.company_read(),
            "grading_summary": MockCompanyDataBuilder.company_grading_read(),
            "general_news": [],
            "price_target_news": [],
            "grading_news": [],
        }
        defaults.update(overrides)
        return CompanyPageResponse(**defaults)

    @staticmethod
    def general_news_read(**overrides) -> CompanyGeneralNewsRead:
        """Build CompanyGeneralNewsRead test data."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "news_title": "Test News Title",
            "text": "Test news content...",
            "published_date": "2023-10-01",
            "news_url": "https://test.com/news/1",
            "publisher": "Test Publisher",
            "image": "https://test.com/image.jpg",
            "site": "test.com",
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        default_data.update(overrides)
        return CompanyGeneralNewsRead(**default_data)

    @staticmethod
    def price_target_news_read(**overrides) -> CompanyPriceTargetNewsRead:
        """Build CompanyPriceTargetNewsRead test data."""
        default_data = {
            "id": 1,
            "symbol": "TEST",
            "company_id": 1,
            "published_date": "2023-10-01",
            "news_url": "https://test.com/price-target-news/1",
            "news_title": "Price Target Update",
            "analyst_name": "John Doe",
            "price_target": 150.0,
            "adj_price_target": 145.0,
            "price_when_posted": 140.0,
            "news_publisher": "Test Publisher",
            "news_base_url": "https://test.com",
            "analyst_company": "Test Analyst Co.",
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        default_data.update(overrides)
        return CompanyPriceTargetNewsRead(**default_data)

    @staticmethod
    def grading_news_read(**overrides) -> CompanyGradingNewsRead:
        """Build CompanyGradingNewsRead test data."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "published_date": "2023-10-01",
            "news_url": "https://test.com/grading-news/1",
            "news_title": "Stock Upgraded",
            "news_base_url": "https://test.com",
            "news_publisher": "Test Publisher",
            "new_grade": "A",
            "previous_grade": "B",
            "grading_company": "Test Grading Co.",
            "price_when_posted": 120.0,
            "action": "upgrade",
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        default_data.update(overrides)
        return CompanyGradingNewsRead(**default_data)

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
