import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.db.models import Company
from app.schemas.company import CompanyWrite
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class CompanyRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_company_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company by its stock symbol."""
        try:
            return self._db.query(Company).filter(Company.symbol == symbol).first()
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

    def get_company_profile_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company profile by its stock symbol."""
        try:
            return self._db.query(Company).filter_by(symbol=symbol).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting company profile by symbol {symbol}: {e}")
            raise

    def get_company_profiles_by_symbols(self, symbols: list[str]) -> list[Company]:
        """Retrieve multiple companies by their stock symbols."""
        try:
            if not symbols:
                return []
            
            statement = select(Company).where(Company.symbol.in_(symbols))
            return self._db.execute(statement).scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting company profiles by symbols {symbols}: {e}")
            raise

    def upsert_company(self, company_data: CompanyWrite) -> Company:
        """Insert or update a company record based on the provided data."""
        try:
            # Check if company exists by symbol
            existing = self._db.query(Company).filter_by(symbol=company_data.symbol).first()
            
            if existing:
                # Update existing company
                map_model(existing, company_data)
                logger.info(f"Updated company {company_data.symbol}")
            else:
                # Create new company
                existing = Company(**company_data.model_dump(exclude_unset=True))
                self._db.add(existing)
                logger.info(f"Created new company {company_data.symbol}")
            
            self._db.commit()
            self._db.refresh(existing)
            return existing
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error upserting company {company_data.symbol}: {e}")
            raise
    
    def get_sector_industry_for_symbols(
        self, symbols: list[str]
    ) -> dict[str, tuple[str | None, str | None]]:
        """Get sector and industry for a list of company symbols.

        Args:
            symbols: List of stock symbols
        Returns:
            Dict mapping symbol to (sector, industry)
        """
        try:
            if not symbols:
                return {}

            stmt = select(Company.symbol, Company.sector, Company.industry).where(
                Company.symbol.in_(symbols)
            )
            results = self._db.execute(stmt).all()

            sector_industry_map = {
                row[0]: (row[1], row[2]) for row in results
            }

            # Fill in missing symbols with (None, None)
            for symbol in symbols:
                if symbol not in sector_industry_map:
                    sector_industry_map[symbol] = (None, None)

            return sector_industry_map
        except SQLAlchemyError as e:
            logger.error(f"Error getting sector/industry for symbols {symbols}: {e}")
            raise
