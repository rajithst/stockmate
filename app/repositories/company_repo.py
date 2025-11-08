from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Company
from app.repositories.base_repo import BaseRepository
from app.schemas.company import CompanyWrite


class CompanyRepository(BaseRepository):
    def __init__(self, db: Session):
        self._db = db

    def get_company_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company by its stock symbol."""
        return self._db.query(Company).filter(Company.symbol == symbol).first()

    def get_company_snapshot_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company along with its related data by its stock symbol."""
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

    def get_company_profile_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company profile by its stock symbol."""
        return self._get_by_field_value(Company, "symbol", symbol)

    def get_company_profiles_by_symbols(self, symbols: list[str]) -> list[Company]:
        """Retrieve multiple companies by their stock symbols."""
        companies = []
        for symbol in symbols:
            company = self._get_by_field_value(Company, "symbol", symbol)
            if company:
                companies.append(company)
        return companies

    def upsert_company(self, company_data: CompanyWrite) -> Company:
        """Insert or update a company record based on the provided data."""
        return self._upsert_single(
            company_data, Company, lambda c: {"symbol": c.symbol}, "upsert_company"
        )
    
    def get_sector_industry_for_symbols(
        self, symbols: list[str]
    ) -> dict[str, tuple[str | None, str | None]]:
        """Get sector and industry for a list of company symbols.

        Args:
            symbols: List of stock symbols
        Returns:
            Dict mapping symbol to (sector, industry)
        """
        if not symbols:
            return {}

        stmt = select(Company.sector, Company.industry).where(Company.symbol.in_(symbols))
        results = self._db.execute(stmt).all()

        sector_industry_map = {
            symbol: (sector, industry) for (sector, industry), symbol in zip(results, symbols)
        }

        # Fill in missing symbols with (None, None)
        for symbol in symbols:
            if symbol not in sector_industry_map:
                sector_industry_map[symbol] = (None, None)

        return sector_industry_map
