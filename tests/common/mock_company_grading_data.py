from app.schemas.grading import CompanyGradingRead, CompanyGradingSummaryRead
from app.db.models.grading import CompanyGrading, CompanyGradingSummary


class MockCompanyGradingDataBuilder:
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
        return CompanyGradingRead(**(default_data | overrides))

    @staticmethod
    def save_company_grading(db_session, **overrides) -> CompanyGrading:
        """Save CompanyGradingRead test data to the database."""
        default_data = {
            "company_id": 1,
            "symbol": "TEST",
            "grade": "A",
            "score": 85.5,
            "recommendation": "BUY",
            "date": "2023-10-01",
        }
        grading_data = {**default_data, **overrides}
        company_grading = CompanyGrading(**grading_data)
        db_session.add(company_grading)
        db_session.commit()
        db_session.refresh(company_grading)
        return company_grading


class MockCompanyGradingSummaryBuilder:
    @staticmethod
    def company_grading_summary_read(**overrides) -> CompanyGradingSummaryRead:
        """Build CompanyGradingSummaryRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "strong_buy": 5,
            "buy": 3,
            "hold": 1,
            "sell": 0,
            "strong_sell": 0,
            "consensus": "Strong Buy",
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        return CompanyGradingSummaryRead(**(default_data | overrides))

    @staticmethod
    def save_company_grading_summary(db_session, **overrides) -> CompanyGradingSummary:
        """Save CompanyGradingSummaryRead test data to the database."""
        default_data = {
            "company_id": 1,
            "symbol": "TEST",
            "strong_buy": 5,
            "buy": 3,
            "hold": 1,
            "sell": 0,
            "strong_sell": 0,
            "consensus": "Strong Buy",
        }
        grading_summary_data = {**default_data, **overrides}
        company_grading_summary = CompanyGradingSummary(**grading_summary_data)
        db_session.add(company_grading_summary)
        db_session.commit()
        db_session.refresh(company_grading_summary)
        return company_grading_summary
