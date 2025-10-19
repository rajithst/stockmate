from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from app.schemas.company import CompanyPageResponse, CompanyRead
from app.schemas.grading import CompanyGradingRead
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)
from app.services.company_page_service import CompanyPageService
from tests.common.mock_company_data import MockCompanyDataBuilder


class TestCompanyPageService:
    """Test suite for CompanyPageService."""

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session."""
        return MagicMock(spec=Session)

    @pytest.fixture
    def service(self, mock_db_session):
        """Create CompanyPageService instance with mock session."""
        return CompanyPageService(session=mock_db_session)

    @pytest.fixture
    def mock_page_repo(self):
        """Fixture for mocked CompanyPageRepository."""
        with patch(
            "app.services.company_page_service.CompanyPageRepository"
        ) as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo_class.return_value = mock_repo
            yield mock_repo

    @pytest.fixture
    def mock_news_repo(self):
        """Fixture for mocked CompanyNewsRepository."""
        with patch(
            "app.services.company_page_service.CompanyNewsRepository"
        ) as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo_class.return_value = mock_repo
            yield mock_repo

    def test_get_company_page_success(self, mock_page_repo, mock_news_repo, service):
        """Test successful retrieval of company page data."""
        # Arrange
        mock_company_data = MockCompanyDataBuilder.company_read(
            symbol="AAPL", name="Apple Inc."
        )
        mock_grading_data = MockCompanyDataBuilder.company_grading_read(
            symbol="AAPL", grade="A", score=95.0
        )
        mock_news_data = {
            "general": [
                MockCompanyDataBuilder.general_news_read(
                    id=1, symbol="AAPL", news_title="Apple launches new product"
                )
            ],
            "price_target": [
                MockCompanyDataBuilder.price_target_news_read(
                    id=1, symbol="AAPL", news_title="Apple price target raised"
                )
            ],
            "grading": [
                MockCompanyDataBuilder.grading_news_read(
                    id=1, symbol="AAPL", news_title="Apple stock upgraded"
                )
            ],
        }
        mock_page_repo.get_company_profile_snapshot.return_value = (
            mock_company_data,
            mock_grading_data,
        )
        mock_news_repo.get_general_news_by_symbol.return_value = mock_news_data[
            "general"
        ]
        mock_news_repo.get_price_target_news_by_symbol.return_value = mock_news_data[
            "price_target"
        ]
        mock_news_repo.get_grading_news_by_symbol.return_value = mock_news_data[
            "grading"
        ]

        # Act
        result = service.get_company_page("AAPL")

        # Assert
        assert isinstance(result, CompanyPageResponse)
        assert isinstance(result.company, CompanyRead)
        assert isinstance(result.grading_summary, CompanyGradingRead)
        assert len(result.general_news) == 1
        assert len(result.price_target_news) == 1
        assert len(result.grading_news) == 1
        assert isinstance(result.general_news[0], CompanyGeneralNewsRead)
        assert isinstance(result.price_target_news[0], CompanyPriceTargetNewsRead)
        assert isinstance(result.grading_news[0], CompanyGradingNewsRead)

        # Verify repository calls
        mock_page_repo.get_company_profile_snapshot.assert_called_once_with("AAPL")
        mock_news_repo.get_general_news_by_symbol.assert_called_once_with("AAPL")
        mock_news_repo.get_price_target_news_by_symbol.assert_called_once_with("AAPL")
        mock_news_repo.get_grading_news_by_symbol.assert_called_once_with("AAPL")

    def test_get_company_page_not_found(self, mock_page_repo, service):
        """Test get_company_page when company is not found."""
        # Arrange
        mock_page_repo.get_company_profile_snapshot.return_value = None

        # Act
        result = service.get_company_page("INVALID")

        # Assert
        assert result is None
        mock_page_repo.get_company_profile_snapshot.assert_called_once_with("INVALID")

    def test_get_company_page_no_news(self, mock_page_repo, mock_news_repo, service):
        """Test get_company_page with no news data."""
        # Arrange
        mock_company_data = MockCompanyDataBuilder.company_read(
            symbol="AAPL", name="Apple Inc."
        )
        mock_grading_data = MockCompanyDataBuilder.company_grading_read(
            symbol="AAPL", grade="A", score=95.0
        )
        mock_page_repo.get_company_profile_snapshot.return_value = (
            mock_company_data,
            mock_grading_data,
        )

        mock_news_repo.get_general_news_by_symbol.return_value = []
        mock_news_repo.get_price_target_news_by_symbol.return_value = []
        mock_news_repo.get_grading_news_by_symbol.return_value = []

        # Act
        result = service.get_company_page("AAPL")

        # Assert
        assert isinstance(result, CompanyPageResponse)
        assert len(result.general_news) == 0
        assert len(result.price_target_news) == 0
        assert len(result.grading_news) == 0

    def test_get_company_page_repository_initialization(
        self, mock_page_repo, mock_news_repo, service
    ):
        """Test that repositories are properly initialized with database session."""
        # Arrange
        mock_company_data = MockCompanyDataBuilder.company_read(
            symbol="AAPL", name="Apple Inc."
        )
        mock_grading_data = MockCompanyDataBuilder.company_grading_read(
            symbol="AAPL", grade="A", score=95.0
        )
        mock_page_repo.get_company_profile_snapshot.return_value = (
            mock_company_data,
            mock_grading_data,
        )

        mock_news_repo.get_general_news_by_symbol.return_value = []
        mock_news_repo.get_price_target_news_by_symbol.return_value = []
        mock_news_repo.get_grading_news_by_symbol.return_value = []

        # Act
        _ = service.get_company_page("AAPL")

        # Assert
        mock_page_repo.get_company_profile_snapshot.assert_called_once_with("AAPL")
        mock_news_repo.get_general_news_by_symbol.assert_called_once_with("AAPL")
        mock_news_repo.get_price_target_news_by_symbol.assert_called_once_with("AAPL")
        mock_news_repo.get_grading_news_by_symbol.assert_called_once_with("AAPL")

    def test_service_initialization(self, mock_db_session):
        """Test CompanyPageService initialization."""
        # Act
        service = CompanyPageService(session=mock_db_session)

        # Assert
        assert service._db == mock_db_session

    @pytest.mark.parametrize("symbol", ["AAPL", "GOOGL", "MSFT", "TSLA"])
    def test_get_company_page_various_symbols(self, service, symbol):
        """Test get_company_page with various valid symbols."""
        with patch(
            "app.services.company_page_service.CompanyPageRepository"
        ) as mock_page_repo_class:
            # Arrange
            mock_page_repo = MagicMock()
            mock_page_repo.get_company_profile_snapshot.return_value = None
            mock_page_repo_class.return_value = mock_page_repo

            # Act
            result = service.get_company_page(symbol)

            # Assert
            assert result is None
            mock_page_repo.get_company_profile_snapshot.assert_called_once_with(symbol)

    def test_get_company_page_model_validation_error_handling(
        self, mock_page_repo, mock_news_repo, service
    ):
        """Test that model validation errors are properly handled."""
        # Arrange
        invalid_company = MagicMock()
        invalid_company.id = None  # Missing required field
        invalid_company.symbol = None  # Missing required field

        invalid_grading = MagicMock()
        invalid_grading.grade = None  # Missing required field
        invalid_grading.score = "invalid"  # Wrong type

        mock_page_repo.get_company_profile_snapshot.return_value = (
            invalid_company,
            invalid_grading,
        )

        # Act & Assert
        with pytest.raises((ValueError, TypeError)) as exc_info:
            service.get_company_page("TEST")

        # Verify error message and repository calls
        assert "validation" in str(exc_info.value).lower()
        mock_page_repo.get_company_profile_snapshot.assert_called_once_with("TEST")
        mock_news_repo.get_general_news_by_symbol.assert_not_called()
