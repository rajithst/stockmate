from logging import getLogger
from typing import Optional

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.db.models import Company
from app.repositories.company_repo import CompanyRepository
from app.schemas.company import CompanyWrite

logger = getLogger(__name__)


class CompanySyncService:
    """
    Service for synchronizing company data between external API and local database.

    This service handles the business logic for fetching company data from external
    sources and managing its persistence in the local database.
    """

    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        """
        Initialize CompanySyncService with required dependencies.

        Args:
            market_api_client: Client for external market data API
            session: Database session for persistence operations
        """
        self._market_api_client = market_api_client
        self._repository = CompanyRepository(session)

    def upsert_company(self, symbol: str) -> Optional[Company]:
        """
        Fetch company data from external API and upsert it into the database.

        Args:
            symbol: Stock symbol of the company

        Returns:
            Company model if successful, None if company not found

        Raises:
            Exception: If there's an error during API fetch or database operation
        """
        try:
            company_data = self._market_api_client.get_company_profile(symbol)
            if not company_data:
                logger.info(f"No company data found for symbol: {symbol}")
                return None

            company_in = CompanyWrite.model_validate(company_data.model_dump())
            return self._repository.upsert_company(company_in)

        except Exception as e:
            logger.error(f"Error syncing company data for {symbol}: {str(e)}")
            raise

    def delete_company(self, symbol: str) -> Optional[Company]:
        """
        Delete a company from the database by its stock symbol.

        Args:
            symbol: Stock symbol of the company to delete

        Returns:
            Deleted Company model if successful, None if company not found

        Raises:
            Exception: If there's an error during database operation
        """
        try:
            return self._repository.delete_company_by_symbol(symbol)
        except Exception as e:
            logger.error(f"Error deleting company {symbol}: {str(e)}")
            raise
