import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from app.services.company_service import CompanyService
from app.schemas.company import CompanyPageResponse, CompanyRead
from app.schemas.company_metrics import CompanyDiscountedCashFlowRead
from app.schemas.market_data import CompanyGradingSummaryRead
from app.schemas.market_data import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)
from app.schemas.market_data import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.schemas.quote import StockPriceChangeRead
from app.schemas.market_data import CompanyRatingSummaryRead
from tests.common.mock_company_data import MockCompanyDataBuilder
from tests.common.mock_company_grading_data import MockCompanyGradingDataBuilder
from tests.common.mock_company_rating_data import MockCompanyRatingSummaryBuilder
from tests.common.mock_dcf_data import MockDiscountedCashFlowDataBuilder
from tests.common.mock_price_target_data import MockPriceTargetDataBuilder
from tests.common.mock_price_change_data import MockStockPriceChangeDataBuilder
from tests.common.mock_company_news_data import MockCompanyNewsDataBuilder


class TestCompanyService:
    """Test suite for CompanyService."""

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session."""
        return MagicMock(spec=Session)

    @pytest.fixture
    def service(self, mock_db_session):
        """Create CompanyService instance with mock session."""
        return CompanyService(mock_db_session)

    @pytest.fixture
    def mock_company_repo(self):
        """Patch CompanyRepository."""
        with patch("app.services.company_service.CompanyRepository") as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo_class.return_value = mock_repo
            yield mock_repo

    @pytest.fixture
    def mock_news_repo(self):
        """Patch CompanyNewsRepository."""
        with patch(
            "app.services.company_service.CompanyNewsRepository"
        ) as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo_class.return_value = mock_repo
            yield mock_repo

    @pytest.fixture
    def mock_company_with_relations(self):
        """Create a mock company with all relationships."""
        mock_company = MockCompanyDataBuilder.company_model(id=1, symbol="AAPL")

        # Add relationships
        mock_company.grading_summary = (
            MockCompanyGradingDataBuilder.company_grading_summary_model(
                id=1, symbol="AAPL"
            )
        )
        mock_company.discounted_cash_flow = (
            MockDiscountedCashFlowDataBuilder.discounted_cash_flow_model(
                id=1, symbol="AAPL"
            )
        )
        mock_company.rating_summary = (
            MockCompanyRatingSummaryBuilder.company_rating_summary_model(
                id=1, symbol="AAPL"
            )
        )
        mock_company.price_target = MockPriceTargetDataBuilder.price_target_model(
            id=1, symbol="AAPL"
        )
        mock_company.price_target_summary = (
            MockPriceTargetDataBuilder.price_target_summary_model(id=1, symbol="AAPL")
        )
        mock_company.price_change = (
            MockStockPriceChangeDataBuilder.stock_price_change_model(
                id=1, symbol="AAPL"
            )
        )

        return mock_company

    def test_get_company_page_success(
        self, service, mock_company_repo, mock_news_repo, mock_company_with_relations
    ):
        """Test successful retrieval of company page data."""
        # Arrange
        symbol = "AAPL"

        # Mock company repository response
        mock_company_repo.get_company_snapshot_by_symbol.return_value = (
            mock_company_with_relations
        )

        # Mock news repository responses
        mock_general_news = [
            MockCompanyNewsDataBuilder.general_news_model(id=1, symbol=symbol)
        ]
        mock_price_target_news = [
            MockCompanyNewsDataBuilder.price_target_news_model(id=1, symbol=symbol)
        ]
        mock_grading_news = [
            MockCompanyNewsDataBuilder.grading_news_model(id=1, symbol=symbol)
        ]

        mock_news_repo.get_general_news_by_symbol.return_value = mock_general_news
        mock_news_repo.get_price_target_news_by_symbol.return_value = (
            mock_price_target_news
        )
        mock_news_repo.get_grading_news_by_symbol.return_value = mock_grading_news

        # Act
        result = service.get_company_page(symbol)

        # Assert
        assert result is not None
        assert isinstance(result, CompanyPageResponse)

        # Verify company data
        assert isinstance(result.company, CompanyRead)
        assert result.company.symbol == symbol

        # Verify related data
        assert isinstance(result.grading_summary, CompanyGradingSummaryRead)
        assert isinstance(result.dcf, CompanyDiscountedCashFlowRead)
        assert isinstance(result.rating_summary, CompanyRatingSummaryRead)
        assert isinstance(result.price_target, CompanyPriceTargetRead)
        assert isinstance(result.price_target_summary, CompanyPriceTargetSummaryRead)
        assert isinstance(result.price_change, StockPriceChangeRead)

        # Verify news data
        assert len(result.general_news) == 1
        assert len(result.price_target_news) == 1
        assert len(result.grading_news) == 1
        assert isinstance(result.general_news[0], CompanyGeneralNewsRead)
        assert isinstance(result.price_target_news[0], CompanyPriceTargetNewsRead)
        assert isinstance(result.grading_news[0], CompanyGradingNewsRead)

        # Verify repository calls
        mock_company_repo.get_company_snapshot_by_symbol.assert_called_once_with(symbol)
        mock_news_repo.get_general_news_by_symbol.assert_called_once_with(symbol)
        mock_news_repo.get_price_target_news_by_symbol.assert_called_once_with(symbol)
        mock_news_repo.get_grading_news_by_symbol.assert_called_once_with(symbol)

    def test_get_company_page_company_not_found(
        self, service, mock_company_repo, mock_news_repo
    ):
        """Test company page retrieval when company doesn't exist."""
        # Arrange
        symbol = "NONEXISTENT"
        mock_company_repo.get_company_snapshot_by_symbol.return_value = None

        # Act
        result = service.get_company_page(symbol)

        # Assert
        assert result is None
        mock_company_repo.get_company_snapshot_by_symbol.assert_called_once_with(symbol)

        # Verify news repos are not called when company is not found
        mock_news_repo.get_general_news_by_symbol.assert_not_called()
        mock_news_repo.get_price_target_news_by_symbol.assert_not_called()
        mock_news_repo.get_grading_news_by_symbol.assert_not_called()

    def test_get_company_page_with_empty_news(
        self, service, mock_company_repo, mock_news_repo, mock_company_with_relations
    ):
        """Test company page retrieval with no news items."""
        # Arrange
        symbol = "AAPL"
        mock_company_repo.get_company_snapshot_by_symbol.return_value = (
            mock_company_with_relations
        )

        # Empty news lists
        mock_news_repo.get_general_news_by_symbol.return_value = []
        mock_news_repo.get_price_target_news_by_symbol.return_value = []
        mock_news_repo.get_grading_news_by_symbol.return_value = []

        # Act
        result = service.get_company_page(symbol)

        # Assert
        assert result is not None
        assert isinstance(result, CompanyPageResponse)
        assert result.company.symbol == symbol
        assert len(result.general_news) == 0
        assert len(result.price_target_news) == 0
        assert len(result.grading_news) == 0

    def test_get_company_page_with_multiple_news_items(
        self, service, mock_company_repo, mock_news_repo, mock_company_with_relations
    ):
        """Test handling of multiple news items."""
        # Arrange
        symbol = "AAPL"
        mock_company_repo.get_company_snapshot_by_symbol.return_value = (
            mock_company_with_relations
        )

        # Multiple news items
        mock_general_news = [
            MockCompanyNewsDataBuilder.general_news_model(symbol=symbol, id=1),
            MockCompanyNewsDataBuilder.general_news_model(symbol=symbol, id=2),
            MockCompanyNewsDataBuilder.general_news_model(symbol=symbol, id=3),
        ]
        mock_price_target_news = [
            MockCompanyNewsDataBuilder.price_target_news_model(symbol=symbol, id=1),
            MockCompanyNewsDataBuilder.price_target_news_model(symbol=symbol, id=2),
        ]
        mock_grading_news = [
            MockCompanyNewsDataBuilder.grading_news_model(symbol=symbol, id=1),
        ]

        mock_news_repo.get_general_news_by_symbol.return_value = mock_general_news
        mock_news_repo.get_price_target_news_by_symbol.return_value = (
            mock_price_target_news
        )
        mock_news_repo.get_grading_news_by_symbol.return_value = mock_grading_news

        # Act
        result = service.get_company_page(symbol)

        # Assert
        assert len(result.general_news) == 3
        assert len(result.price_target_news) == 2
        assert len(result.grading_news) == 1
        assert all(
            isinstance(news, CompanyGeneralNewsRead) for news in result.general_news
        )
        assert all(
            isinstance(news, CompanyPriceTargetNewsRead)
            for news in result.price_target_news
        )
        assert all(
            isinstance(news, CompanyGradingNewsRead) for news in result.grading_news
        )

    def test_get_company_page_repositories_initialized_with_session(
        self, service, mock_company_repo, mock_news_repo, mock_company_with_relations
    ):
        """Test that repositories are initialized with correct session."""
        # Arrange
        symbol = "AAPL"
        mock_company_repo.get_company_snapshot_by_symbol.return_value = (
            mock_company_with_relations
        )

        mock_news_repo.get_general_news_by_symbol.return_value = []
        mock_news_repo.get_price_target_news_by_symbol.return_value = []
        mock_news_repo.get_grading_news_by_symbol.return_value = []

        # Act
        with (
            patch("app.services.company_service.CompanyRepository") as CompanyRepoClass,
            patch(
                "app.services.company_service.CompanyNewsRepository"
            ) as NewsRepoClass,
        ):
            CompanyRepoClass.return_value = mock_company_repo
            NewsRepoClass.return_value = mock_news_repo

            service.get_company_page(symbol)

            # Assert repositories were initialized with session
            CompanyRepoClass.assert_called_once_with(service._db)
            NewsRepoClass.assert_called_once_with(service._db)

    @pytest.mark.parametrize("symbol", ["AAPL", "GOOGL", "MSFT", "TSLA"])
    def test_get_company_page_with_different_symbols(
        self, service, mock_company_repo, mock_news_repo, symbol
    ):
        """Test company page retrieval with various stock symbols."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_model(id=1, symbol=symbol)
        mock_company.grading_summary = (
            MockCompanyGradingDataBuilder.company_grading_summary_model(
                id=1, symbol=symbol
            )
        )
        mock_company.discounted_cash_flow = (
            MockDiscountedCashFlowDataBuilder.discounted_cash_flow_model(
                id=1, symbol=symbol
            )
        )
        mock_company.rating_summary = (
            MockCompanyRatingSummaryBuilder.company_rating_summary_model(
                id=1, symbol=symbol
            )
        )
        mock_company.price_target = MockPriceTargetDataBuilder.price_target_model(
            id=1, symbol=symbol
        )
        mock_company.price_target_summary = (
            MockPriceTargetDataBuilder.price_target_summary_model(id=1, symbol=symbol)
        )
        mock_company.price_change = (
            MockStockPriceChangeDataBuilder.stock_price_change_model(
                id=1, symbol=symbol
            )
        )

        mock_company_repo.get_company_snapshot_by_symbol.return_value = mock_company

        mock_news_repo.get_general_news_by_symbol.return_value = []
        mock_news_repo.get_price_target_news_by_symbol.return_value = []
        mock_news_repo.get_grading_news_by_symbol.return_value = []

        # Act
        result = service.get_company_page(symbol)

        # Assert
        assert result is not None
        assert result.company.symbol == symbol
        mock_company_repo.get_company_snapshot_by_symbol.assert_called_once_with(symbol)

    def test_get_company_page_validates_all_schema_types(
        self, service, mock_company_repo, mock_news_repo, mock_company_with_relations
    ):
        """Test that all response data is properly validated to schema types."""
        # Arrange
        symbol = "AAPL"
        mock_company_repo.get_company_snapshot_by_symbol.return_value = (
            mock_company_with_relations
        )

        mock_news_repo.get_general_news_by_symbol.return_value = []
        mock_news_repo.get_price_target_news_by_symbol.return_value = []
        mock_news_repo.get_grading_news_by_symbol.return_value = []

        # Act
        result = service.get_company_page(symbol)

        # Assert - verify all schema types
        assert isinstance(result, CompanyPageResponse)
        assert isinstance(result.company, CompanyRead)
        assert isinstance(result.grading_summary, CompanyGradingSummaryRead)
        assert isinstance(result.dcf, CompanyDiscountedCashFlowRead)
        assert isinstance(result.rating_summary, CompanyRatingSummaryRead)
        assert isinstance(result.price_target, CompanyPriceTargetRead)
        assert isinstance(result.price_target_summary, CompanyPriceTargetSummaryRead)
        assert isinstance(result.price_change, StockPriceChangeRead)

    def test_get_company_page_service_uses_correct_session(self, mock_db_session):
        """Test that service stores and uses the correct database session."""
        # Arrange & Act
        service = CompanyService(mock_db_session)

        # Assert
        assert service._db is mock_db_session
