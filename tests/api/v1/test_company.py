from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.company import get_company_service
from app.main import app
from data.company_test_data import get_company_read


@pytest.fixture
def mock_company_service():
    """Provide a mock CompanyService via FastAPI dependency override."""
    mock_service = MagicMock()
    app.dependency_overrides[get_company_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.clear()  # clean up after test


@pytest.mark.usefixtures("client")
class TestCompanyProfileAPI:
    """Test suite for /profile/{symbol} endpoint."""

    def test_get_company_profile_success(
        self, client: TestClient, mock_company_service: MagicMock
    ):
        """Fetch an existing company profile."""
        mock_company = get_company_read(id=1, symbol="AAPL", company_name="Apple Inc.")
        mock_company_service.get_company_profile.return_value = mock_company

        response = client.get("/api/v1/company/AAPL")

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert data["company_name"] == "Apple Inc."

    def test_get_company_profile_not_found(
        self, client: TestClient, mock_company_service: MagicMock
    ):
        """Fetch a non-existent company profile."""
        mock_company_service.get_company_profile.return_value = None

        response = client.get("/api/v1/company/INVALID")

        assert response.status_code == 404
        assert response.json()["detail"] == "Company not found"
