from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)
from app.db.models.news import (
    CompanyGeneralNews,
    CompanyGradingNews,
    CompanyPriceTargetNews,
)


class MockCompanyNewsDataBuilder:
    @staticmethod
    def grading_news_read(**overrides) -> CompanyGradingNewsRead:
        """Build CompanyGradingNewsRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "published_date": "2023-10-01T12:00:00Z",
            "news_url": "https://example.com/article",
            "news_title": "Company Achieves New Milestone",
            "news_base_url": "https://example.com",
            "news_publisher": "Finance News Daily",
            "new_grade": "A",
            "previous_grade": "B",
            "grading_company": "Top Graders Inc.",
            "action": "Upgraded",
            "price_when_posted": 145.00,
            "created_at": "2023-10-01T12:00:00Z",
            "updated_at": "2023-10-01T12:00:00Z",
        }
        return CompanyGradingNewsRead(**(default_data | overrides))

    @staticmethod
    def price_target_news_read(**overrides) -> CompanyPriceTargetNewsRead:
        """Build CompanyPriceTargetNewsRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "TEST",
            "published_date": "2023-10-02T15:30:00Z",
            "news_url": "https://example.com/article",
            "news_title": "Analyst Raises Price Target",
            "analyst_name": "John Doe",
            "price_target": 150.00,
            "adj_price_target": 148.50,
            "price_when_posted": 140.00,
            "news_publisher": "Finance News Daily",
            "news_base_url": "https://example.com",
            "analyst_company": "Top Analysts Inc.",
            "sentiment": "Positive",
            "created_at": "2023-10-02T15:30:00Z",
            "updated_at": "2023-10-02T15:30:00Z",
        }
        return CompanyPriceTargetNewsRead(**(default_data | overrides))

    @staticmethod
    def general_news_read(**overrides) -> CompanyGeneralNewsRead:
        """Build CompanyGeneralNewsRead test data with optional overrides."""
        default_data = {
            "id": 1,
            "company_id": 1,
            "symbol": "AAPL",
            "news_title": "Company Launches New Product",
            "text": "The company has launched a new innovative product.",
            "published_date": "2023-10-03T09:00:00Z",
            "publisher": "Tech News Daily",
            "image": "https://example.com/image.jpg",
            "site": "https://example.com/article",
            "news_url": "https://example.com/article",
            "sentiment": "Positive",
            "created_at": "2023-10-03T09:00:00Z",
            "updated_at": "2023-10-03T09:00:00Z",
        }
        return CompanyGeneralNewsRead(**(default_data | overrides))

    @staticmethod
    def save_grading_news(db_session, **overrides) -> CompanyGradingNews:
        """Save CompanyGradingNewsRead test data to the database."""
        default_data = {
            "company_id": 1,
            "symbol": "TEST",
            "published_date": "2023-10-01T12:00:00Z",
            "news_url": "https://example.com/article",
            "news_title": "Company Achieves New Milestone",
            "news_base_url": "https://example.com",
            "news_publisher": "Finance News Daily",
            "new_grade": "A",
            "previous_grade": "B",
            "grading_company": "Top Graders Inc.",
            "action": "Upgraded",
            "price_when_posted": 145.00,
        }
        grading_news_data = {**default_data, **overrides}
        grading_news = CompanyGradingNews(**grading_news_data)
        db_session.add(grading_news)
        db_session.commit()
        db_session.refresh(grading_news)
        return grading_news

    @staticmethod
    def save_price_target_news(db_session, **overrides) -> CompanyPriceTargetNews:
        """Save CompanyPriceTargetNewsRead test data to the database."""
        default_data = {
            "company_id": 1,
            "symbol": "TEST",
            "published_date": "2023-10-02T15:30:00Z",
            "news_url": "https://example.com/article",
            "news_title": "Analyst Raises Price Target",
            "analyst_name": "John Doe",
            "price_target": 150.00,
            "adj_price_target": 148.50,
            "price_when_posted": 140.00,
            "news_publisher": "Finance News Daily",
            "news_base_url": "https://example.com",
            "analyst_company": "Top Analysts Inc.",
            "sentiment": "Positive",
        }
        price_target_news_data = {**default_data, **overrides}
        price_target_news = CompanyPriceTargetNews(**price_target_news_data)
        db_session.add(price_target_news)
        db_session.commit()
        db_session.refresh(price_target_news)
        return price_target_news

    @staticmethod
    def save_general_news(db_session, **overrides) -> CompanyGeneralNews:
        """Save CompanyGeneralNewsRead test data to the database."""
        default_data = {
            "company_id": 1,
            "symbol": "AAPL",
            "news_title": "Company Launches New Product",
            "text": "The company has launched a new innovative product.",
            "published_date": "2023-10-03T09:00:00Z",
            "publisher": "Tech News Daily",
            "image": "https://example.com/image.jpg",
            "site": "https://example.com/article",
            "news_url": "https://example.com/article",
            "sentiment": "Positive",
        }
        general_news_data = {**default_data, **overrides}
        general_news = CompanyGeneralNews(**general_news_data)
        db_session.add(general_news)
        db_session.commit()
        db_session.refresh(general_news)
        return general_news
