from app.schemas.rating import CompanyRatingSummaryRead
from app.db.models.ratings import CompanyRatingSummary


class MockCompanyRatingSummaryBuilder:
    @staticmethod
    def company_rating_summary_read(**overrides) -> CompanyRatingSummaryRead:
        """Build CompanyRatingSummaryRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "rating": "Buy",
            "overall_score": 4,
            "discounted_cash_flow_score": 4,
            "return_on_equity_score": 4,
            "return_on_assets_score": 4,
            "debt_to_equity_score": 3,
            "price_to_earnings_score": 4,
            "price_to_book_score": 4,
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        return CompanyRatingSummaryRead(**(default_data | overrides))

    @staticmethod
    def save_company_rating(db_session, **overrides) -> CompanyRatingSummaryRead:
        """Save CompanyRatingSummaryRead test data to the database."""
        default_data = {
            "company_id": 1,
            "symbol": "TEST",
            "rating": "Buy",
            "overall_score": 4,
            "discounted_cash_flow_score": 4,
            "return_on_equity_score": 4,
            "return_on_assets_score": 4,
            "debt_to_equity_score": 3,
            "price_to_earnings_score": 4,
            "price_to_book_score": 4,
        }
        rating_data = {**default_data, **overrides}
        company_rating = CompanyRatingSummary(**rating_data)
        db_session.add(company_rating)
        db_session.commit()
        db_session.refresh(company_rating)
        return company_rating
