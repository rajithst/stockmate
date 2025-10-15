from app.services.company_page_service import CompanyPageService
from data.company_test_data import create_company


class TestCompanyService:
    """Tests for CompanyService using real SQLite test DB."""

    def test_get_company_profile_found(self, db_session):
        # Arrange
        create_company(db_session, symbol="AAPL", company_name="Apple Inc.")
        service = CompanyPageService(session=db_session)

        # Act
        result = service.get_company_profile("AAPL")

        # Assert
        assert result is not None
        assert result.symbol == "AAPL"
        assert result.company_name == "Apple Inc."

    def test_get_company_profile_not_found(self, db_session):
        # Arrange
        service = CompanyPageService(session=db_session)

        # Act
        result = service.get_company_profile("UNKNOWN")

        # Assert
        assert result is None
