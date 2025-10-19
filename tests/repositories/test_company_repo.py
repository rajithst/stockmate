from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from app.db.models.company import Company
from app.repositories.company_repo import CompanyRepository
from tests.common.mock_company_data import MockCompanyDataBuilder


class TestCompanyRepository:
    """Test suite for CompanyRepository."""

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session."""
        return MagicMock(spec=Session)

    @pytest.fixture
    def repository(self, mock_db_session):
        """Create CompanyRepository instance with mock session."""
        return CompanyRepository(db=mock_db_session)

    def test_get_company_by_symbol_found(self, repository, mock_db_session):
        """Test retrieving an existing company by symbol."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_model(
            symbol="AAPL", company_name="Apple Inc."
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_company
        )

        # Act
        result = repository.get_company_by_symbol("AAPL")

        # Assert
        assert result == mock_company
        mock_db_session.query.assert_called_once_with(Company)
        mock_db_session.query.return_value.filter.assert_called_once()
        mock_db_session.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_company_by_symbol_not_found(self, repository, mock_db_session):
        """Test retrieving a non-existent company by symbol."""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = repository.get_company_by_symbol("INVALID")

        # Assert
        assert result is None
        mock_db_session.query.assert_called_once_with(Company)

    def test_get_company_by_symbols_found(self, repository, mock_db_session):
        """Test retrieving multiple companies by symbols."""
        # Arrange
        mock_companies = [
            MockCompanyDataBuilder.company_model(
                symbol="AAPL", company_name="Apple Inc."
            ),
            MockCompanyDataBuilder.company_model(
                symbol="GOOGL", company_name="Alphabet Inc."
            ),
        ]
        mock_db_session.query.return_value.filter.return_value.all.return_value = (
            mock_companies
        )

        # Act
        result = repository.get_company_by_symbols(["AAPL", "GOOGL"])

        # Assert
        assert result == mock_companies
        mock_db_session.query.assert_called_once_with(Company)
        mock_db_session.query.return_value.filter.assert_called_once()
        mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

    def test_get_company_by_symbols_empty_list(self, repository, mock_db_session):
        """Test retrieving companies with empty symbols list."""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.all.return_value = []

        # Act
        result = repository.get_company_by_symbols([])

        # Assert
        assert result == []

    def test_upsert_company_creates_new(self, repository, mock_db_session):
        """Test upserting a new company (insert case)."""
        # Arrange
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        company_write = MockCompanyDataBuilder.company_write(
            symbol="NEWCO", company_name="New Company Inc."
        )
        new_company = MockCompanyDataBuilder.company_model(
            symbol="NEWCO", company_name="New Company Inc."
        )

        with patch("app.repositories.company_repo.Company") as mock_company_class:
            mock_company_class.return_value = new_company

            # Act
            result = repository.upsert_company(company_write)

            # Assert
            assert result == new_company
            mock_company_class.assert_called_once_with(
                **company_write.model_dump(exclude_unset=True)
            )
            mock_db_session.add.assert_called_once_with(new_company)
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once_with(new_company)

    def test_upsert_company_updates_existing(self, repository, mock_db_session):
        """Test upserting an existing company (update case)."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_model(
            symbol="AAPL", company_name="Apple Inc."
        )
        company_write = MockCompanyDataBuilder.company_write(
            symbol="AAPL", company_name="Apple Incorporated"
        )
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_company
        )

        with patch("app.repositories.company_repo.map_model") as mock_map_model:
            mock_map_model.return_value = mock_company

            # Act
            result = repository.upsert_company(company_write)

            # Assert
            assert result == mock_company
            mock_map_model.assert_called_once_with(mock_company, company_write)
            mock_db_session.add.assert_not_called()  # Should not add existing company
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once_with(mock_company)

    def test_delete_company_by_symbol_found(self, repository, mock_db_session):
        """Test deleting an existing company by symbol."""
        # Arrange
        mock_company = MockCompanyDataBuilder.company_model(
            symbol="AAPL", company_name="Apple Inc."
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_company
        )

        # Act
        result = repository.delete_company_by_symbol("AAPL")

        # Assert
        assert result == mock_company
        mock_db_session.query.assert_called_once_with(Company)
        mock_db_session.delete.assert_called_once_with(mock_company)
        mock_db_session.commit.assert_called_once()

    def test_delete_company_by_symbol_not_found(self, repository, mock_db_session):
        """Test deleting a non-existent company by symbol."""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = repository.delete_company_by_symbol("INVALID")

        # Assert
        assert result is None
        mock_db_session.query.assert_called_once_with(Company)
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()

    def test_repository_initialization(self, mock_db_session):
        """Test CompanyRepository initialization."""
        # Act
        repository = CompanyRepository(db=mock_db_session)

        # Assert
        assert repository._db == mock_db_session

    @pytest.mark.parametrize("symbol", ["AAPL", "aapl", "123", "TEST.L"])
    def test_get_company_by_symbol_various_formats(
        self, repository, mock_db_session, symbol
    ):
        """Test get_company_by_symbol with various symbol formats."""
        # Arrange
        mock_company = MagicMock(spec=Company, symbol=symbol)
        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_company
        )

        # Act
        result = repository.get_company_by_symbol(symbol)

        # Assert
        assert result == mock_company


class TestCompanyRepositoryIntegration:
    """Integration tests for CompanyRepository using real database session."""

    def test_get_company_by_symbol_integration(self, db_session):
        """Test get_company_by_symbol with real database."""
        # Arrange
        created_company = MockCompanyDataBuilder.save_company(
            db_session, symbol="INTEG", company_name="Integration Test Corp"
        )
        repository = CompanyRepository(db=db_session)

        # Act
        result = repository.get_company_by_symbol("INTEG")

        # Assert
        assert result is not None
        assert result.symbol == "INTEG"
        assert result.company_name == "Integration Test Corp"
        assert result.id == created_company.id

    def test_get_company_by_symbols_integration(self, db_session):
        """Test get_company_by_symbols with real database."""
        # Arrange
        MockCompanyDataBuilder.save_company(
            db_session, symbol="INTEG1", company_name="Integration One"
        )
        MockCompanyDataBuilder.save_company(
            db_session, symbol="INTEG2", company_name="Integration Two"
        )
        repository = CompanyRepository(db=db_session)

        # Act
        result = repository.get_company_by_symbols(["INTEG1", "INTEG2", "NONEXISTENT"])

        # Assert
        assert len(result) == 2
        symbols = [company.symbol for company in result]
        assert "INTEG1" in symbols
        assert "INTEG2" in symbols
        assert "NONEXISTENT" not in symbols

    def test_upsert_company_insert_integration(self, db_session):
        """Test upsert_company insert with real database."""
        # Arrange
        repository = CompanyRepository(db=db_session)
        company_data = MockCompanyDataBuilder.company_write(
            symbol="NEWCO", company_name="New Company Inc.", price=100.0
        )

        # Act
        result = repository.upsert_company(company_data)

        # Assert
        assert result.id is not None
        assert result.symbol == "NEWCO"
        assert result.company_name == "New Company Inc."
        assert result.price == 100.0

    def test_upsert_company_update_integration(self, db_session):
        """Test upsert_company update with real database."""
        # Arrange
        existing = MockCompanyDataBuilder.save_company(
            db_session, symbol="EXISTING", company_name="Existing Company", price=50.0
        )
        repository = CompanyRepository(db=db_session)

        company_data = MockCompanyDataBuilder.company_write(
            symbol="EXISTING", company_name="Updated Company Inc.", price=75.0
        )

        # Act
        result = repository.upsert_company(company_data)

        # Assert
        assert result.id == existing.id  # Same record
        assert result.symbol == "EXISTING"
        assert result.company_name == "Updated Company Inc."
        assert result.price == 75.0  # Updated price

    def test_delete_company_integration(self, db_session):
        """Test delete_company_by_symbol with real database."""
        # Arrange
        created_company = MockCompanyDataBuilder.save_company(
            db_session, symbol="DELETEME", company_name="Delete Me Inc."
        )
        repository = CompanyRepository(db=db_session)

        # Act
        result = repository.delete_company_by_symbol("DELETEME")

        # Assert
        assert result is not None
        assert result.id == created_company.id

        # Verify company is actually deleted
        deleted_company = repository.get_company_by_symbol("DELETEME")
        assert deleted_company is None
