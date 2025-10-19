from app.schemas.price_target import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.db.models.price_target import CompanyPriceTarget, CompanyPriceTargetSummary


class MockPriceTargetDataBuilder:
    @staticmethod
    def price_target_read(**overrides) -> CompanyPriceTargetRead:
        """Build CompanyPriceTargetRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "target_high": 150.0,
            "target_low": 100.0,
            "target_consensus": 125.0,
            "target_median": 130.0,
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        return CompanyPriceTargetRead(**(default_data | overrides))

    @staticmethod
    def save_price_target(db_session, **overrides) -> CompanyPriceTarget:
        """Save CompanyPriceTargetRead test data to the database."""

        default_data = {
            "company_id": 1,
            "symbol": "TEST",
            "target_high": 150.0,
            "target_low": 100.0,
            "target_consensus": 125.0,
            "target_median": 130.0,
        }
        price_target_data = {**default_data, **overrides}
        price_target = CompanyPriceTarget(**price_target_data)
        db_session.add(price_target)
        db_session.commit()
        db_session.refresh(price_target)
        return price_target


class MockPriceTargetSummaryDataBuilder:
    @staticmethod
    def price_target_summary_read(**overrides) -> CompanyPriceTargetSummaryRead:
        """Build CompanyPriceTargetSummaryRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "last_month_count": 5,
            "last_month_average_price_target": 128.0,
            "last_quarter_count": 15,
            "last_quarter_average_price_target": 130.0,
            "last_year_count": 60,
            "last_year_average_price_target": 127.5,
            "all_time_count": 200,
            "all_time_average_price_target": 125.0,
            "publishers": "Analyst A, Analyst B",
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        return CompanyPriceTargetSummaryRead(**(default_data | overrides))

    @staticmethod
    def save_price_target_summary(db_session, **overrides) -> CompanyPriceTargetSummary:
        """Save CompanyPriceTargetSummaryRead test data to the database."""

        default_data = {
            "company_id": 1,
            "symbol": "TEST",
            "last_month_count": 5,
            "last_month_average_price_target": 128.0,
            "last_quarter_count": 15,
            "last_quarter_average_price_target": 130.0,
            "last_year_count": 60,
            "last_year_average_price_target": 127.5,
            "all_time_count": 200,
            "all_time_average_price_target": 125.0,
            "publishers": "Analyst A, Analyst B",
        }
        price_target_summary_data = {**default_data, **overrides}
        price_target_summary = CompanyPriceTarget(**price_target_summary_data)
        db_session.add(price_target_summary)
        db_session.commit()
        db_session.refresh(price_target_summary)
        return price_target_summary
