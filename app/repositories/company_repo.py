from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.db.models import Company
from app.schemas.company import CompanyWrite
from app.util.map_model import map_model


class CompanyRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_company_snapshot_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company along with its related data by its stock symbol."""
        statement = (
            select(Company)
            .options(
                joinedload(Company.grading_summary),
                joinedload(Company.discounted_cash_flow),
                joinedload(Company.rating_summary),
                joinedload(Company.price_target),
                joinedload(Company.price_target_summary),
                joinedload(Company.price_change),
            )
            .where(Company.symbol == symbol)
        )

        return self._db.execute(statement).scalars().first()

    def get_company_financials_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company along with its financial data by its stock symbol."""
        pass

    def get_company_profile_by_symbol(self, symbol: str) -> Company | None:
        """Retrieve a company by its stock symbol."""
        return self._db.query(Company).filter(Company.symbol == symbol).first()

    def get_company_profiles_by_symbols(self, symbols: list[str]) -> list[Company]:
        """Retrieve multiple companies by their stock symbols."""
        return self._db.query(Company).filter(Company.symbol.in_(symbols)).all()

    def upsert_company(self, company_data: CompanyWrite) -> Company:
        """Insert or update a company record based on the provided data."""
        existing = self._db.query(Company).filter_by(symbol=company_data.symbol).first()

        if existing:
            company = map_model(existing, company_data)
        else:
            company = Company(**company_data.model_dump(exclude_unset=True))
            self._db.add(company)

        self._db.commit()
        self._db.refresh(company)

        return company

    def delete_company_by_symbol(self, symbol: str) -> Company | None:
        """Delete a company by its stock symbol."""
        company = self._db.query(Company).filter(Company.symbol == symbol).first()
        if company:
            self._db.delete(company)
            self._db.commit()
            return company
        return None
