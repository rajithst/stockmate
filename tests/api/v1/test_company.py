from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.api.v1.company import get_company_service
from app.main import app
from app.services.company_service import CompanyService
from tests.common.mock_company_data import MockCompanyDataBuilder
from tests.common.mock_company_grading_data import MockCompanyGradingSummaryBuilder
from tests.common.mock_company_page_data import MockCompanyPageDataBuilder


class TestCompanyAPI:
    """Comprehensive test suite for Company API endpoints."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return Mock(spec=Session)

    @pytest.fixture
    def mock_company_service(self):
        """Create a mock CompanyPageService."""
        return Mock(spec=CompanyService)

    def test_get_company_service_creation(self, mock_session):
        # Arrange & Act
        service = get_company_service(session=mock_session)

        # Assert
        assert isinstance(service, CompanyService)
        assert service._db == mock_session

    @pytest.fixture(autouse=True)
    def setup_dependency_override(self, mock_company_service):
        """Override the company service dependency for testing."""
        app.dependency_overrides[get_company_service] = lambda: mock_company_service
        yield
        app.dependency_overrides.clear()

    def test_get_company_profile_success_complete_data(
        self, client, mock_company_service
    ):
        """Test successful company profile retrieval with complete data."""
        # Arrange
        company_read = MockCompanyDataBuilder.company_read(
            symbol="AAPL", company_name="Apple Inc."
        )
        mock_page_response = MockCompanyPageDataBuilder.company_page_response(
            company=company_read
        )
        mock_company_service.get_company_page.return_value = mock_page_response

        # Act
        response = client.get("/api/v1/company/AAPL")

        # Assert
        assert response.status_code == 200
        data = response.json()
        print(data)

        # Verify company data
        assert data["company"]["symbol"] == "AAPL"
        assert data["company"]["company_name"] == "Apple Inc."

        mock_company_service.get_company_page.assert_called_once_with("AAPL")

    def test_get_company_profile_not_found(self, client, mock_company_service):
        """Test company profile not found scenario."""
        # Arrange
        mock_company_service.get_company_page.return_value = None

        # Act
        response = client.get("/api/v1/company/INVALID")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Company not found"
        mock_company_service.get_company_page.assert_called_once_with("INVALID")

    @pytest.mark.parametrize(
        "symbol", ["AAPL", "GOOGL", "MSFT", "TSLA", "BRK.A", "BRK-B"]
    )
    def test_get_company_profile_various_valid_symbols(
        self, client, mock_company_service, symbol
    ):
        """Test API with various valid symbol formats."""
        # Arrange
        mock_company_service.get_company_page.return_value = None

        # Act
        response = client.get(f"/api/v1/company/{symbol}")

        # Assert
        assert response.status_code == 404  # Since we return None
        mock_company_service.get_company_page.assert_called_once_with(symbol)

    @pytest.mark.parametrize("invalid_symbol", ["!@$", "123456789012345678901"])
    def test_get_company_profile_invalid_symbols(
        self, client, mock_company_service, invalid_symbol
    ):
        """Test API with invalid symbol formats."""
        # Arrange
        mock_company_service.get_company_page.return_value = None

        # Act
        response = client.get(f"/api/v1/company/{invalid_symbol}")

        # Assert
        # The API should still process these, but service returns None
        assert response.status_code == 404
        mock_company_service.get_company_page.assert_called_once_with(invalid_symbol)

    def test_get_company_profile_service_exception(self, client, mock_company_service):
        """Test API behavior when service raises an exception."""
        # Arrange
        mock_company_service.get_company_page.side_effect = Exception(
            "Database connection error"
        )

        # Act & Assert
        with pytest.raises(Exception, match="Database connection error"):
            _ = client.get("/api/v1/company/AAPL")

    def test_get_company_profile_service_validation_error(
        self, client, mock_company_service
    ):
        """Test API behavior when service has validation errors."""
        # Arrange
        mock_company_service.get_company_page.side_effect = ValueError(
            "Invalid data format"
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid data format"):
            _ = client.get("/api/v1/company/AAPL")

    def test_dependency_injection(self, mock_session):
        """Test that the dependency injection works correctly."""
        # Act
        service = get_company_service(session=mock_session)

        # Assert
        assert isinstance(service, CompanyService)
        assert service._db == mock_session

    def test_router_configuration(self):
        """Test that the router is configured correctly."""
        from app.api.v1.company import router

        # Assert
        assert router.prefix == "/company"

        # Check that the route exists
        routes = [route.path for route in router.routes]
        assert "/company/{symbol}" in routes

    def test_response_model_validation(self, client, mock_company_service):
        """Test that response follows the CompanyPageResponse model."""
        # Arrange
        valid_response = MockCompanyPageDataBuilder.company_page_response(
            company=MockCompanyDataBuilder.company_read(symbol="TEST"),
            grading_summary=MockCompanyGradingSummaryBuilder.company_grading_summary_read(symbol="TEST"),
            general_news=[],
            price_target_news=[],
            grading_news=[],
        )
        mock_company_service.get_company_page.return_value = valid_response

        # Act
        response = client.get("/api/v1/company/AAPL")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Verify response structure matches CompanyPageResponse
        required_keys = [
            "company",
            "grading_summary",
            "general_news",
            "price_target_news",
            "grading_news",
        ]
        assert all(key in data for key in required_keys)

    def test_http_methods(self, client, mock_company_service):
        """Test that only GET method is allowed."""
        # Arrange
        mock_company_service.get_company_page.return_value = None

        # Test allowed method
        get_response = client.get("/api/v1/company/AAPL")
        assert get_response.status_code in [200, 404]  # Valid response codes

        # Test disallowed methods
        post_response = client.post("/api/v1/company/AAPL")
        assert post_response.status_code == 405  # Method Not Allowed

        put_response = client.put("/api/v1/company/AAPL")
        assert put_response.status_code == 405  # Method Not Allowed

        delete_response = client.delete("/api/v1/company/AAPL")
        assert delete_response.status_code == 405  # Method Not Allowed
