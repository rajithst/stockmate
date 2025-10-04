import pytest
from app.services.company_service import CompanyService
from data.company_test_data import create_company
from tests.test_db import TestingSessionLocal, init_test_db


@pytest.fixture(scope="function")
def db_session():
    """Provide a fresh DB session for each test."""
    init_test_db()  # clean slate each time
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class TestCompanyService:
    """Tests for CompanyService using real SQLite test DB."""

    def test_get_company_profile_found(self, db_session):
        # Arrange
        create_company(db_session, symbol="AAPL", company_name="Apple Inc.")
        service = CompanyService(session=db_session)

        # Act
        result = service.get_company_profile("AAPL")

        # Assert
        assert result is not None
        assert result.symbol == "AAPL"
        assert result.company_name == "Apple Inc."

    def test_get_company_profile_not_found(self, db_session):
        # Arrange
        service = CompanyService(session=db_session)

        # Act
        result = service.get_company_profile("UNKNOWN")

        # Assert
        assert result is None
