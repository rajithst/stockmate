import pytest
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session

from app.db.models.company import Company
from app.repositories.company_repo import CompanyRepository
from tests.common.mock_company_data import MockCompanyDataBuilder


class TestCompanyRepositoryUnit:
    """Unit tests for CompanyRepository using mocks."""

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session."""
        return MagicMock(spec=Session)

    @pytest.fixture
    def repository(self, mock_db_session):
        """Create CompanyRepository instance with mock session."""
        return CompanyRepository(db=mock_db_session)

    @pytest.fixture
    def mock_company(self):
        """Create a mock company (not a real SQLAlchemy model)."""
        return MockCompanyDataBuilder.company_mock(
            id=1, symbol="AAPL", company_name="Apple Inc.", price=150.0
        )

    @pytest.fixture
    def mock_select(self):
        """Patch select function."""
        with patch("app.repositories.company_repo.select") as mock:
            yield mock

    @pytest.fixture
    def mock_joinedload(self):
        """Patch joinedload function."""
        with patch("app.repositories.company_repo.joinedload") as mock:
            yield mock

    @pytest.fixture
    def mock_company_class(self):
        """Patch Company class."""
        with patch("app.repositories.company_repo.Company") as mock:
            yield mock

    @pytest.fixture
    def mock_map_model(self):
        """Patch map_model function."""
        with patch("app.repositories.company_repo.map_model") as mock:
            yield mock

    # ===== Test: get_company_snapshot_by_symbol =====

    def test_get_company_snapshot_by_symbol_with_all_relations(
        self, repository, mock_db_session, mock_select, mock_joinedload
    ):
        """Test retrieving company snapshot with all relationships loaded."""
        # Arrange
        symbol = "AAPL"
        mock_company = MockCompanyDataBuilder.company_mock(id=1, symbol=symbol)

        # Mock relationships (now works because it's a Mock object)
        mock_company.grading_summary = Mock()
        mock_company.discounted_cash_flow = Mock()
        mock_company.rating_summary = Mock()
        mock_company.price_target = Mock()
        mock_company.price_target_summary = Mock()
        mock_company.price_change = Mock()

        # Mock the query chain
        mock_result = Mock()
        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_company
        mock_result.scalars.return_value = mock_scalars
        mock_db_session.execute.return_value = mock_result

        mock_stmt = Mock()
        mock_select.return_value = mock_stmt
        mock_stmt.options.return_value = mock_stmt
        mock_stmt.where.return_value = mock_stmt

        # Act
        result = repository.get_company_snapshot_by_symbol(symbol)

        # Assert
        assert result == mock_company
        assert result.symbol == symbol
        mock_select.assert_called_once_with(Company)
        assert mock_joinedload.call_count == 6  # 6 relationships
        mock_db_session.execute.assert_called_once()
        mock_scalars.first.assert_called_once()

    def test_get_company_snapshot_by_symbol_not_found(
        self, repository, mock_db_session, mock_select, mock_joinedload
    ):
        """Test retrieving company snapshot when company doesn't exist."""
        # Arrange
        mock_result = Mock()
        mock_scalars = Mock()
        mock_scalars.first.return_value = None
        mock_result.scalars.return_value = mock_scalars
        mock_db_session.execute.return_value = mock_result

        mock_stmt = Mock()
        mock_select.return_value = mock_stmt
        mock_stmt.options.return_value = mock_stmt
        mock_stmt.where.return_value = mock_stmt

        # Act
        result = repository.get_company_snapshot_by_symbol("NONEXISTENT")

        # Assert
        assert result is None
        mock_scalars.first.assert_called_once()

    @pytest.mark.parametrize(
        "symbol,company_id",
        [("AAPL", 1), ("GOOGL", 2), ("MSFT", 3), ("TSLA", 4), ("BRK.B", 5)],
    )
    def test_get_company_snapshot_by_symbol_various_symbols(
        self,
        repository,
        mock_db_session,
        mock_select,
        mock_joinedload,
        symbol,
        company_id,
    ):
        """Test retrieving company snapshot with various symbols."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_mock(id=company_id, symbol=symbol)
        mock_company.grading_summary = Mock()
        mock_company.discounted_cash_flow = Mock()
        mock_company.rating_summary = Mock()
        mock_company.price_target = Mock()
        mock_company.price_target_summary = Mock()
        mock_company.price_change = Mock()

        mock_result = Mock()
        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_company
        mock_result.scalars.return_value = mock_scalars
        mock_db_session.execute.return_value = mock_result

        mock_stmt = Mock()
        mock_select.return_value = mock_stmt
        mock_stmt.options.return_value = mock_stmt
        mock_stmt.where.return_value = mock_stmt

        # Act
        result = repository.get_company_snapshot_by_symbol(symbol)

        # Assert
        assert result is not None
        assert result.symbol == symbol
        assert result.id == company_id

    # ===== Test: get_company_profile_by_symbol =====

    def test_get_company_profile_by_symbol_found(
        self, repository, mock_db_session, mock_company
    ):
        """Test retrieving an existing company profile by symbol."""
        # Arrange
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_company

        # Act
        result = repository.get_company_profile_by_symbol("AAPL")

        # Assert
        assert result == mock_company
        assert result.symbol == "AAPL"
        assert result.company_name == "Apple Inc."
        mock_db_session.query.assert_called_once_with(Company)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()

    def test_get_company_profile_by_symbol_not_found(self, repository, mock_db_session):
        """Test retrieving a non-existent company profile by symbol."""
        # Arrange
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        # Act
        result = repository.get_company_profile_by_symbol("INVALID")

        # Assert
        assert result is None
        mock_db_session.query.assert_called_once_with(Company)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()

    @pytest.mark.parametrize(
        "symbol,company_id,name",
        [
            ("AAPL", 1, "Apple Inc."),
            ("GOOGL", 2, "Alphabet Inc."),
            ("MSFT", 3, "Microsoft Corporation"),
        ],
    )
    def test_get_company_profile_by_symbol_various_companies(
        self, repository, mock_db_session, symbol, company_id, name
    ):
        """Test retrieving various company profiles."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_mock(
            id=company_id, symbol=symbol, company_name=name
        )
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_company

        # Act
        result = repository.get_company_profile_by_symbol(symbol)

        # Assert
        assert result.id == company_id
        assert result.symbol == symbol
        assert result.company_name == name

    # ===== Test: get_company_profiles_by_symbols =====

    def test_get_company_profiles_by_symbols_multiple_found(
        self, repository, mock_db_session
    ):
        """Test retrieving multiple company profiles by symbols."""
        # Arrange
        mock_companies = [
            MockCompanyDataBuilder.company_mock(
                id=1, symbol="AAPL", company_name="Apple Inc."
            ),
            MockCompanyDataBuilder.company_mock(
                id=2, symbol="GOOGL", company_name="Alphabet Inc."
            ),
            MockCompanyDataBuilder.company_mock(
                id=3, symbol="MSFT", company_name="Microsoft Corp."
            ),
        ]
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.all.return_value = mock_companies

        # Act
        result = repository.get_company_profiles_by_symbols(["AAPL", "GOOGL", "MSFT"])

        # Assert
        assert result == mock_companies
        assert len(result) == 3
        assert result[0].id == 1
        assert result[0].symbol == "AAPL"
        assert result[1].id == 2
        assert result[1].symbol == "GOOGL"
        assert result[2].id == 3
        assert result[2].symbol == "MSFT"
        mock_db_session.query.assert_called_once_with(Company)
        mock_query.filter.assert_called_once()
        mock_filter.all.assert_called_once()

    def test_get_company_profiles_by_symbols_empty_list(
        self, repository, mock_db_session
    ):
        """Test retrieving companies with empty symbols list."""
        # Arrange
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.all.return_value = []

        # Act
        result = repository.get_company_profiles_by_symbols([])

        # Assert
        assert result == []
        mock_db_session.query.assert_called_once_with(Company)

    def test_get_company_profiles_by_symbols_single_symbol(
        self, repository, mock_db_session
    ):
        """Test retrieving companies with single symbol."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_mock(id=1, symbol="AAPL")
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.all.return_value = [mock_company]

        # Act
        result = repository.get_company_profiles_by_symbols(["AAPL"])

        # Assert
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].symbol == "AAPL"

    def test_get_company_profiles_by_symbols_partial_found(
        self, repository, mock_db_session
    ):
        """Test retrieving companies where only some symbols exist."""
        # Arrange
        mock_companies = [
            MockCompanyDataBuilder.company_mock(id=1, symbol="AAPL"),
            MockCompanyDataBuilder.company_mock(id=2, symbol="GOOGL"),
        ]
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.all.return_value = mock_companies

        # Act
        result = repository.get_company_profiles_by_symbols(
            ["AAPL", "GOOGL", "INVALID"]
        )

        # Assert
        assert len(result) == 2
        symbols = [company.symbol for company in result]
        assert "AAPL" in symbols
        assert "GOOGL" in symbols
        assert "INVALID" not in symbols

    def test_get_company_profiles_by_symbols_duplicate_handling(
        self, repository, mock_db_session
    ):
        """Test retrieving companies with duplicate symbols in input."""
        # Arrange
        mock_companies = [
            MockCompanyDataBuilder.company_mock(id=1, symbol="AAPL"),
        ]
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.all.return_value = mock_companies

        # Act
        result = repository.get_company_profiles_by_symbols(["AAPL", "AAPL", "AAPL"])

        # Assert
        assert len(result) == 1  # Should return only one company
        assert result[0].id == 1
        assert result[0].symbol == "AAPL"

    # ===== Test: upsert_company (INSERT) =====

    def test_upsert_company_creates_new(
        self, repository, mock_db_session, mock_company_class
    ):
        """Test upserting a new company (insert case)."""
        # Arrange
        company_write = MockCompanyDataBuilder.company_write(
            symbol="NEWCO", company_name="New Company Inc.", price=100.0
        )

        mock_query = mock_db_session.query.return_value
        mock_filter_by = mock_query.filter_by.return_value
        mock_filter_by.first.return_value = None

        new_company = MockCompanyDataBuilder.company_mock(
            id=10, symbol="NEWCO", company_name="New Company Inc.", price=100.0
        )
        mock_company_class.return_value = new_company

        # Act
        result = repository.upsert_company(company_write)

        # Assert
        assert result == new_company
        assert result.id == 10
        mock_company_class.assert_called_once_with(
            **company_write.model_dump(exclude_unset=True)
        )
        mock_db_session.add.assert_called_once_with(new_company)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(new_company)

    def test_upsert_company_creates_with_all_fields(
        self, repository, mock_db_session, mock_company_class
    ):
        """Test upserting a new company with all fields."""
        # Arrange
        company_write = MockCompanyDataBuilder.company_write(
            symbol="FULL",
            company_name="Full Company Inc.",
            price=150.0,
            market_cap=5000000000,
            industry="Technology",
            website="https://full.com",
            sector="Technology",
            country="United States",
        )

        mock_query = mock_db_session.query.return_value
        mock_filter_by = mock_query.filter_by.return_value
        mock_filter_by.first.return_value = None

        new_company = MockCompanyDataBuilder.company_mock(
            id=20, **company_write.model_dump()
        )
        mock_company_class.return_value = new_company

        # Act
        result = repository.upsert_company(company_write)

        # Assert
        assert result.id == 20
        assert result.symbol == "FULL"
        assert result.price == 150.0
        assert result.market_cap == 5000000000
        assert result.industry == "Technology"
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    # ===== Test: upsert_company (UPDATE) =====

    def test_upsert_company_updates_existing(
        self, repository, mock_db_session, mock_map_model
    ):
        """Test upserting an existing company (update case)."""
        # Arrange
        existing_company = MockCompanyDataBuilder.company_mock(
            id=1, symbol="AAPL", company_name="Apple Inc.", price=150.0
        )

        company_write = MockCompanyDataBuilder.company_write(
            symbol="AAPL", company_name="Apple Incorporated", price=175.0
        )

        mock_query = mock_db_session.query.return_value
        mock_filter_by = mock_query.filter_by.return_value
        mock_filter_by.first.return_value = existing_company
        mock_map_model.return_value = existing_company

        # Act
        result = repository.upsert_company(company_write)

        # Assert
        assert result == existing_company
        assert result.id == 1
        mock_map_model.assert_called_once_with(existing_company, company_write)
        mock_db_session.add.assert_not_called()  # Should not add existing
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(existing_company)

    def test_upsert_company_updates_all_fields(
        self, repository, mock_db_session, mock_map_model
    ):
        """Test upserting updates all fields when all are provided."""
        # Arrange
        existing_company = MockCompanyDataBuilder.company_mock(
            id=1, symbol="AAPL", company_name="Old Name", price=100.0
        )

        company_write = MockCompanyDataBuilder.company_write(
            symbol="AAPL", company_name="New Name", price=200.0, market_cap=3000000000
        )

        mock_query = mock_db_session.query.return_value
        mock_filter_by = mock_query.filter_by.return_value
        mock_filter_by.first.return_value = existing_company
        mock_map_model.return_value = existing_company

        # Act
        result = repository.upsert_company(company_write)

        # Assert
        assert result.id == 1
        mock_map_model.assert_called_once()
        mock_db_session.commit.assert_called_once()

    # ===== Test: delete_company_by_symbol =====

    def test_delete_company_by_symbol_found(
        self, repository, mock_db_session, mock_company
    ):
        """Test deleting an existing company by symbol."""
        # Arrange
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_company

        # Act
        result = repository.delete_company_by_symbol("AAPL")

        # Assert
        assert result == mock_company
        assert result.id == 1
        mock_db_session.query.assert_called_once_with(Company)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_db_session.delete.assert_called_once_with(mock_company)
        mock_db_session.commit.assert_called_once()

    def test_delete_company_by_symbol_not_found(self, repository, mock_db_session):
        """Test deleting a non-existent company by symbol."""
        # Arrange
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        # Act
        result = repository.delete_company_by_symbol("INVALID")

        # Assert
        assert result is None
        mock_db_session.query.assert_called_once_with(Company)
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()

    def test_delete_company_by_symbol_multiple_calls(self, repository, mock_db_session):
        """Test deleting multiple companies sequentially."""
        # Arrange
        company1 = MockCompanyDataBuilder.company_mock(id=1, symbol="AAPL")
        company2 = MockCompanyDataBuilder.company_mock(id=2, symbol="GOOGL")

        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.side_effect = [company1, company2]

        # Act
        result1 = repository.delete_company_by_symbol("AAPL")
        result2 = repository.delete_company_by_symbol("GOOGL")

        # Assert
        assert result1 == company1
        assert result1.id == 1
        assert result2 == company2
        assert result2.id == 2
        assert mock_db_session.delete.call_count == 2
        assert mock_db_session.commit.call_count == 2

    @pytest.mark.parametrize(
        "symbol,company_id", [("AAPL", 1), ("GOOGL", 2), ("MSFT", 3), ("TSLA", 4)]
    )
    def test_delete_company_by_symbol_various_symbols(
        self, repository, mock_db_session, symbol, company_id
    ):
        """Test deleting companies with various symbols."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_mock(id=company_id, symbol=symbol)
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_company

        # Act
        result = repository.delete_company_by_symbol(symbol)

        # Assert
        assert result.id == company_id
        assert result.symbol == symbol
        mock_db_session.delete.assert_called_once_with(mock_company)
        mock_db_session.commit.assert_called_once()

    # ===== Test: Repository Initialization =====

    def test_repository_initialization(self, mock_db_session):
        """Test CompanyRepository initialization."""
        # Act
        repository = CompanyRepository(db=mock_db_session)

        # Assert
        assert repository._db == mock_db_session
        assert hasattr(repository, "_db")

    def test_repository_initialization_with_none_session(self):
        """Test CompanyRepository initialization with None session."""
        # Act & Assert
        repository = CompanyRepository(db=None)
        assert repository._db is None

    # ===== Test: Error Handling =====

    def test_upsert_company_commit_failure(
        self, repository, mock_db_session, mock_company_class
    ):
        """Test upsert_company handles commit failures."""
        # Arrange
        company_write = MockCompanyDataBuilder.company_write(symbol="FAIL")
        mock_query = mock_db_session.query.return_value
        mock_filter_by = mock_query.filter_by.return_value
        mock_filter_by.first.return_value = None

        new_company = MockCompanyDataBuilder.company_mock(id=99, symbol="FAIL")
        mock_company_class.return_value = new_company
        mock_db_session.commit.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.upsert_company(company_write)

        assert "Database error" in str(exc_info.value)

    def test_delete_company_commit_failure(
        self, repository, mock_db_session, mock_company
    ):
        """Test delete_company_by_symbol handles commit failures."""
        # Arrange
        mock_query = mock_db_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_company
        mock_db_session.commit.side_effect = Exception("Delete failed")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.delete_company_by_symbol("AAPL")

        assert "Delete failed" in str(exc_info.value)

    def test_get_company_profile_query_failure(self, repository, mock_db_session):
        """Test get_company_profile_by_symbol handles query failures."""
        # Arrange
        mock_db_session.query.side_effect = Exception("Query error")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.get_company_profile_by_symbol("AAPL")

        assert "Query error" in str(exc_info.value)
