import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.db.models import Company
from app.db.models.company import NonUSCompany

logger = logging.getLogger(__name__)


class CompanyRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_all_companies(self) -> list[Company]:
        """Retrieve all companies"""
        try:
            statement = select(Company)
            return self._db.execute(statement).scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting all companies: {e}")
            raise

    def get_all_non_us_companies(self) -> list[str]:
        """Retrieve all non-US companies"""
        try:
            statement = select(
                NonUSCompany.symbol,
            )
            return [row[0] for row in self._db.execute(statement).all()]
        except SQLAlchemyError as e:
            logger.error(f"Error getting all non-US companies: {e}")
            raise

    def get_company_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company by its stock symbol."""
        try:
            return self._db.query(Company).filter(Company.symbol == symbol).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting company by symbol {symbol}: {e}")
            raise

    def get_companies_by_symbols(self, symbols: list[str]) -> list[Company]:
        """Retrieve multiple companies by their stock symbols."""
        try:
            if not symbols:
                return []

            statement = select(Company).where(Company.symbol.in_(symbols))
            return self._db.execute(statement).scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting company profiles by symbols {symbols}: {e}")
            raise

    def get_non_us_company_by_symbol(self, symbol) -> NonUSCompany | None:
        """Retrieve a non-US company by its stock symbol."""
        try:
            return (
                self._db.query(NonUSCompany)
                .filter(NonUSCompany.symbol == symbol)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting company by symbol {symbol}: {e}")
            raise

    def get_company_snapshot_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company along with its related data by its stock symbol."""
        try:
            statement = (
                select(Company)
                .options(
                    selectinload(Company.grading_summary),
                    selectinload(Company.discounted_cash_flow),
                    selectinload(Company.rating_summary),
                    selectinload(Company.price_target),
                    selectinload(Company.price_target_summary),
                    selectinload(Company.stock_price_change),
                )
                .where(Company.symbol == symbol)
            )
            return self._db.execute(statement).scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting company snapshot by symbol {symbol}: {e}")
            raise
