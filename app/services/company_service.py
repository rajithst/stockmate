from sqlalchemy.orm import Session

from app.repositories.company_repo import CompanyRepository
from app.schemas.company import CompanyRead


class CompanyService:
    def __init__(self, session: Session):
        self._db = session

    def get_company_profile(self, symbol: str) -> CompanyRead | None:
        """Retrieve a company's profile by its stock symbol."""
        repository = CompanyRepository(self._db)
        company = repository.get_company_by_symbol(symbol)
        if company:
            return CompanyRead.model_validate(company, from_attributes=True)
        return None