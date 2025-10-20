from typing import Type, TypeVar, Any, Dict
from sqlalchemy.orm import Session

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

T = TypeVar("T")


class MockCompanyNewsDataBuilder:
    """Builder for creating test data for company news with minimal duplication."""

    # Define default data for each news type
    _GRADING_NEWS_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "published_date": "2023-10-01T12:00:00",
        "news_url": "https://example.com/article",
        "news_title": "Company Achieves New Milestone",
        "news_base_url": "https://example.com",
        "news_publisher": "Finance News Daily",
        "new_grade": "A",
        "previous_grade": "B",
        "grading_company": "Top Graders Inc.",
        "action": "Upgraded",
        "sentiment": "Positive",
        "price_when_posted": 145.00,
        "created_at": "2023-10-01T12:00:00",
        "updated_at": "2023-10-01T12:00:00",
    }

    _PRICE_TARGET_NEWS_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "TEST",
        "published_date": "2023-10-02T15:30:00",
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
        "created_at": "2023-10-02T15:30:00",
        "updated_at": "2023-10-02T15:30:00",
    }

    _GENERAL_NEWS_DEFAULTS = {
        "id": 1,
        "company_id": 1,
        "symbol": "AAPL",
        "news_title": "Company Launches New Product",
        "text": "The company has launched a new innovative product.",
        "published_date": "2023-10-03T09:00:00",
        "publisher": "Tech News Daily",
        "image": "https://example.com/image.jpg",
        "site": "https://example.com/article",
        "news_url": "https://example.com/article",
        "sentiment": "Positive",
        "created_at": "2023-10-03T09:00:00",
        "updated_at": "2023-10-03T09:00:00",
    }

    @staticmethod
    def _create_model(
        model_class: Type[T], defaults: Dict[str, Any], overrides: Dict[str, Any]
    ) -> T:
        """
        Generic method to create a model instance.

        Args:
            model_class: The SQLAlchemy model class to instantiate
            defaults: Default values for the model
            overrides: Values to override defaults

        Returns:
            Model instance with merged data
        """
        data = {**defaults, **overrides}
        model = model_class(**data)
        # Manually set id since it's usually auto-generated
        if "id" in data:
            model.id = data["id"]
        return model

    @staticmethod
    def _create_schema(
        schema_class: Type[T], defaults: Dict[str, Any], overrides: Dict[str, Any]
    ) -> T:
        """
        Generic method to create a Pydantic schema instance.

        Args:
            schema_class: The Pydantic schema class to instantiate
            defaults: Default values for the schema
            overrides: Values to override defaults

        Returns:
            Schema instance with merged data
        """
        return schema_class(**(defaults | overrides))

    @staticmethod
    def _save_to_db(
        db_session: Session,
        model_class: Type[T],
        defaults: Dict[str, Any],
        overrides: Dict[str, Any],
    ) -> T:
        """
        Generic method to save a model to database.

        Args:
            db_session: Database session
            model_class: The SQLAlchemy model class to instantiate
            defaults: Default values for the model
            overrides: Values to override defaults

        Returns:
            Saved and refreshed model instance
        """
        # Remove fields that shouldn't be set when creating
        data = {**defaults, **overrides}
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        model = model_class(**data)
        db_session.add(model)
        db_session.commit()
        db_session.refresh(model)
        return model

    # ===== Grading News =====
    @staticmethod
    def grading_news_model(**overrides) -> CompanyGradingNews:
        """
        Create a CompanyGradingNews model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Contains analyst grade changes (upgrades/downgrades) for companies.

        Args:
            **overrides: Override default values for any grading news attributes.
                Common overrides: symbol, new_grade, previous_grade, grading_company,
                action, sentiment, published_date

        Returns:
            CompanyGradingNews: SQLAlchemy model instance

        Examples:
            >>> news = MockCompanyNewsDataBuilder.grading_news_model(
            ...     symbol="AAPL",
            ...     new_grade="A+",
            ...     previous_grade="A",
            ...     action="Upgraded"
            ... )
            >>> assert isinstance(news, CompanyGradingNews)
            >>> assert news.action == "Upgraded"
        """
        return MockCompanyNewsDataBuilder._create_model(
            CompanyGradingNews,
            MockCompanyNewsDataBuilder._GRADING_NEWS_DEFAULTS,
            overrides,
        )

    @staticmethod
    def grading_news_read(**overrides) -> CompanyGradingNewsRead:
        """
        Create a CompanyGradingNewsRead schema instance.

        Use for testing API responses that return grading news data.
        Represents analyst grade changes in API output format.

        Args:
            **overrides: Override default values for any grading news attributes.
                Common overrides: symbol, new_grade, previous_grade, grading_company,
                action, sentiment, published_date

        Returns:
            CompanyGradingNewsRead: Pydantic schema for API output

        Examples:
            >>> news_read = MockCompanyNewsDataBuilder.grading_news_read(
            ...     symbol="GOOGL",
            ...     action="Downgraded",
            ...     sentiment="Negative"
            ... )
            >>> assert isinstance(news_read, CompanyGradingNewsRead)
            >>> assert news_read.sentiment == "Negative"
        """
        return MockCompanyNewsDataBuilder._create_schema(
            CompanyGradingNewsRead,
            MockCompanyNewsDataBuilder._GRADING_NEWS_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_grading_news(db_session: Session, **overrides) -> CompanyGradingNews:
        """
        Save CompanyGradingNews to database.

        Use for integration tests that require database persistence.
        Automatically removes auto-generated fields (id, timestamps) before insertion.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any grading news attributes.
                Common overrides: symbol, new_grade, previous_grade, grading_company,
                action, sentiment, published_date

        Returns:
            CompanyGradingNews: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> news = MockCompanyNewsDataBuilder.save_grading_news(
            ...     db_session,
            ...     symbol="MSFT",
            ...     new_grade="B+",
            ...     grading_company="Goldman Sachs"
            ... )
            >>> assert news.id is not None  # ID assigned by database
            >>> assert news.created_at is not None
        """
        return MockCompanyNewsDataBuilder._save_to_db(
            db_session,
            CompanyGradingNews,
            MockCompanyNewsDataBuilder._GRADING_NEWS_DEFAULTS,
            overrides,
        )

    # ===== Price Target News =====
    @staticmethod
    def price_target_news_model(**overrides) -> CompanyPriceTargetNews:
        """
        Create a CompanyPriceTargetNews model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Contains analyst price target updates and revisions for companies.

        Args:
            **overrides: Override default values for any price target news attributes.
                Common overrides: symbol, analyst_name, price_target, adj_price_target,
                analyst_company, sentiment, published_date

        Returns:
            CompanyPriceTargetNews: SQLAlchemy model instance

        Examples:
            >>> news = MockCompanyNewsDataBuilder.price_target_news_model(
            ...     symbol="TSLA",
            ...     analyst_name="Jane Smith",
            ...     price_target=250.00,
            ...     analyst_company="Morgan Stanley"
            ... )
            >>> assert isinstance(news, CompanyPriceTargetNews)
            >>> assert news.price_target == 250.00
        """
        return MockCompanyNewsDataBuilder._create_model(
            CompanyPriceTargetNews,
            MockCompanyNewsDataBuilder._PRICE_TARGET_NEWS_DEFAULTS,
            overrides,
        )

    @staticmethod
    def price_target_news_read(**overrides) -> CompanyPriceTargetNewsRead:
        """
        Create a CompanyPriceTargetNewsRead schema instance.

        Use for testing API responses that return price target news data.
        Represents analyst price target updates in API output format.

        Args:
            **overrides: Override default values for any price target news attributes.
                Common overrides: symbol, analyst_name, price_target, adj_price_target,
                analyst_company, sentiment, published_date

        Returns:
            CompanyPriceTargetNewsRead: Pydantic schema for API output

        Examples:
            >>> news_read = MockCompanyNewsDataBuilder.price_target_news_read(
            ...     symbol="NFLX",
            ...     price_target=450.00,
            ...     sentiment="Positive"
            ... )
            >>> assert isinstance(news_read, CompanyPriceTargetNewsRead)
            >>> assert news_read.price_target == 450.00
        """
        return MockCompanyNewsDataBuilder._create_schema(
            CompanyPriceTargetNewsRead,
            MockCompanyNewsDataBuilder._PRICE_TARGET_NEWS_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_price_target_news(
        db_session: Session, **overrides
    ) -> CompanyPriceTargetNews:
        """
        Save CompanyPriceTargetNews to database.

        Use for integration tests that require database persistence.
        Automatically removes auto-generated fields (id, timestamps) before insertion.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any price target news attributes.
                Common overrides: symbol, analyst_name, price_target, adj_price_target,
                analyst_company, sentiment, published_date

        Returns:
            CompanyPriceTargetNews: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> news = MockCompanyNewsDataBuilder.save_price_target_news(
            ...     db_session,
            ...     symbol="AMZN",
            ...     analyst_name="Bob Johnson",
            ...     price_target=180.00,
            ...     analyst_company="JP Morgan"
            ... )
            >>> assert news.id is not None  # ID assigned by database
            >>> assert news.analyst_name == "Bob Johnson"
        """
        return MockCompanyNewsDataBuilder._save_to_db(
            db_session,
            CompanyPriceTargetNews,
            MockCompanyNewsDataBuilder._PRICE_TARGET_NEWS_DEFAULTS,
            overrides,
        )

    # ===== General News =====
    @staticmethod
    def general_news_model(**overrides) -> CompanyGeneralNews:
        """
        Create a CompanyGeneralNews model instance (without saving to DB).

        Use for integration tests where you need actual SQLAlchemy models.
        Contains general company news articles (product launches, earnings, etc.).

        Args:
            **overrides: Override default values for any general news attributes.
                Common overrides: symbol, news_title, text, publisher, sentiment,
                published_date, image, news_url

        Returns:
            CompanyGeneralNews: SQLAlchemy model instance

        Examples:
            >>> news = MockCompanyNewsDataBuilder.general_news_model(
            ...     symbol="AAPL",
            ...     news_title="Apple Releases New iPhone",
            ...     text="Apple unveiled its latest iPhone model today.",
            ...     sentiment="Positive"
            ... )
            >>> assert isinstance(news, CompanyGeneralNews)
            >>> assert "iPhone" in news.news_title
        """
        return MockCompanyNewsDataBuilder._create_model(
            CompanyGeneralNews,
            MockCompanyNewsDataBuilder._GENERAL_NEWS_DEFAULTS,
            overrides,
        )

    @staticmethod
    def general_news_read(**overrides) -> CompanyGeneralNewsRead:
        """
        Create a CompanyGeneralNewsRead schema instance.

        Use for testing API responses that return general news data.
        Represents general company news articles in API output format.

        Args:
            **overrides: Override default values for any general news attributes.
                Common overrides: symbol, news_title, text, publisher, sentiment,
                published_date, image, news_url

        Returns:
            CompanyGeneralNewsRead: Pydantic schema for API output

        Examples:
            >>> news_read = MockCompanyNewsDataBuilder.general_news_read(
            ...     symbol="META",
            ...     news_title="Meta Announces New AI Features",
            ...     publisher="Tech Crunch"
            ... )
            >>> assert isinstance(news_read, CompanyGeneralNewsRead)
            >>> assert news_read.publisher == "Tech Crunch"
        """
        return MockCompanyNewsDataBuilder._create_schema(
            CompanyGeneralNewsRead,
            MockCompanyNewsDataBuilder._GENERAL_NEWS_DEFAULTS,
            overrides,
        )

    @staticmethod
    def save_general_news(db_session: Session, **overrides) -> CompanyGeneralNews:
        """
        Save CompanyGeneralNews to database.

        Use for integration tests that require database persistence.
        Automatically removes auto-generated fields (id, timestamps) before insertion.

        Args:
            db_session: SQLAlchemy database session
            **overrides: Override default values for any general news attributes.
                Common overrides: symbol, news_title, text, publisher, sentiment,
                published_date, image, news_url

        Returns:
            CompanyGeneralNews: Saved and refreshed SQLAlchemy model with DB-assigned ID

        Examples:
            >>> news = MockCompanyNewsDataBuilder.save_general_news(
            ...     db_session,
            ...     symbol="GOOGL",
            ...     news_title="Google Expands Cloud Services",
            ...     text="Google announces new cloud infrastructure.",
            ...     publisher="Bloomberg"
            ... )
            >>> assert news.id is not None  # ID assigned by database
            >>> assert news.symbol == "GOOGL"
        """
        return MockCompanyNewsDataBuilder._save_to_db(
            db_session,
            CompanyGeneralNews,
            MockCompanyNewsDataBuilder._GENERAL_NEWS_DEFAULTS,
            overrides,
        )
