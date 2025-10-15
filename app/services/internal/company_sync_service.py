from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.db.models import Company
from app.repositories.company_repo import CompanyRepository
from app.schemas.company import CompanyWrite


class CompanySyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        self.market_api_client = market_api_client
        self._db = session

    def upsert_company(self, symbol: str) -> Company | None:
        """Fetches company data from external client and upserts it into the database.
        Returns the upserted Company model or None if not found."""
        fmp_company_data = self.market_api_client.get_company_profile(symbol)
        if fmp_company_data:
            company_in = CompanyWrite.model_validate(fmp_company_data.model_dump())
            repository = CompanyRepository(self._db)
            return repository.upsert_company(company_in)
        return None

    def delete_company(self, symbol: str) -> Company | None:
        """Deletes a company from the database by its stock symbol.
        Returns the deleted Company model or None if not found."""
        repository = CompanyRepository(self._db)
        return repository.delete_company_by_symbol(symbol)
