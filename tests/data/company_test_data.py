from app.db.models.company import Company
from app.schemas.company import CompanyRead
from data.mock_data import mock_company_data


def create_company(db_session, **overrides) -> Company:
    """
    Create and persist a Company instance with default mock data,
    allowing overrides for specific fields.

    Args:
        db_session: SQLAlchemy session object for database operations.
        **overrides: Fields to override in the default mock data.
    Returns:
        The created Company instance.
    """

    company = Company(**{**mock_company_data, **overrides})
    db_session.add(company)
    db_session.commit()
    return company


def get_company_read(**overrides) -> CompanyRead:
    """
    Create a CompanyRead schema instance with default mock data,
    allowing overrides for specific fields.

    Args:
        **overrides: Fields to override in the default mock data.
    Returns:
        The created CompanyRead instance.
    """
    return CompanyRead(**{**mock_company_data, **overrides})
